from datetime import datetime

import pydantic
from fastapi import HTTPException
from prisma.models import Plan as DbPlan
from prisma.types import PlanCreateInput
from pydantic import BaseModel

from app.plan.plan import ValidatablePlan
from app.plan.storable import StorablePlan, migrate_plan
from app.user.key import ModKey, Rut, UserKey

MAX_PLANS_PER_USER = 50

_plan_model_fields = list(DbPlan.__fields__.keys())
# automatic definition of low detail to avoid hardcoding attributes
# something like: ['id', 'created_at', 'updated_at', 'name', 'is_favorite', 'user_rut']
_low_detail_attributes = [
    attr for attr in _plan_model_fields if attr not in ["validatable_plan"]
]


class PlanView(BaseModel):
    """
    Detailed, typed view of a plan in the database.
    The only difference between this type and `DbPlan` (ie. the plan schema) is that
    the type of `PlanView.validatable_plan` is `ValidatablePlan`, while the type of
    `Plan.validatable_plan` is `Json`.
    """

    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    is_favorite: bool
    user_rut: Rut
    validatable_plan: ValidatablePlan

    @staticmethod
    async def from_db(db: DbPlan) -> "PlanView":
        return PlanView(
            id=db.id,
            created_at=db.created_at,
            updated_at=db.updated_at,
            name=db.name,
            is_favorite=db.is_favorite,
            user_rut=Rut(db.user_rut),
            validatable_plan=await migrate_plan(
                pydantic.parse_raw_as(
                    StorablePlan,
                    db.validatable_plan,
                ),
            ),
        )


class LowDetailPlanView(BaseModel):
    """
    Lighter version of the PlanView model.
    This should only contain the required attributes to show the user their plans list
    """

    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    is_favorite: bool

    @staticmethod
    def from_db(db: DbPlan) -> "LowDetailPlanView":
        return LowDetailPlanView(
            id=db.id,
            created_at=db.created_at,
            updated_at=db.updated_at,
            name=db.name,
            is_favorite=db.is_favorite,
        )


async def authorize_plan_access(
    user: UserKey,
    plan_id: str,
    try_mod_access: bool,
) -> DbPlan:
    mod_access = try_mod_access and isinstance(user, ModKey)
    plan = await DbPlan.prisma().find_unique(where={"id": plan_id})
    if not plan or (not mod_access and plan.user_rut != user.rut):
        raise HTTPException(status_code=404, detail="Plan not found in user storage")
    return plan


async def store_plan(plan_name: str, user: UserKey, plan: ValidatablePlan) -> PlanView:
    # TODO: Limit nicely in the frontend too.
    current_count = await DbPlan.prisma().count(where={"user_rut": user.rut})
    if current_count >= MAX_PLANS_PER_USER:
        raise HTTPException(status_code=403, detail="Maximum amount of plans reached")

    data = {
        "name": plan_name,
        "user_rut": user.rut,
        "is_favorite": False,
        "validatable_plan": plan.json(),
    }

    # all model attributes are being used (except for the first three autogenerated)
    assert set(data.keys()) == set(_plan_model_fields[3:])

    plan_data = PlanCreateInput(**data)  # type: ignore
    stored_plan = await DbPlan.prisma().create(data=plan_data)

    return await PlanView.from_db(stored_plan)


async def get_plan_details(
    user: UserKey,
    plan_id: str,
    mod_access: bool = False,
) -> PlanView:
    plan = await authorize_plan_access(user, plan_id, mod_access)
    return await PlanView.from_db(plan)


async def get_user_plans(user: UserKey) -> list[LowDetailPlanView]:
    plans = await DbPlan.prisma().find_many(
        where={
            "user_rut": user.rut,
        },
    )

    return [LowDetailPlanView.from_db(plan) for plan in plans]


async def modify_validatable_plan(
    user: UserKey,
    plan_id: str,
    new_plan: ValidatablePlan,
    mod_access: bool = False,
) -> PlanView:
    await authorize_plan_access(user, plan_id, mod_access)

    updated_plan = await DbPlan.prisma().update(
        where={"id": plan_id},
        data={"validatable_plan": new_plan.json()},
    )
    # Must be true because access was authorized
    assert updated_plan is not None

    return await PlanView.from_db(updated_plan)


async def modify_plan_metadata(
    user: UserKey,
    plan_id: str,
    set_name: str | None,
    set_favorite: bool | None,
    mod_access: bool = False,
) -> PlanView:
    await authorize_plan_access(user, plan_id, mod_access)

    if set_name is not None:
        return await _rename_plan(plan_id=plan_id, new_name=set_name)

    if set_favorite is not None:
        return await _set_favorite_plan(
            user=user,
            plan_id=plan_id,
            favorite=set_favorite,
        )

    raise HTTPException(
        status_code=400,
        detail="Must specify the attribute of Plan to update",
    )


async def _rename_plan(plan_id: str, new_name: str) -> PlanView:
    updated_plan = await DbPlan.prisma().update(
        where={
            "id": plan_id,
        },
        data={
            "name": new_name,
        },
    )

    # Must be true because access was authorized
    assert updated_plan is not None

    return await PlanView.from_db(updated_plan)


async def _set_favorite_plan(user: UserKey, plan_id: str, favorite: bool) -> PlanView:
    # NOTE: with the current algorithm there cannot be more than one favorite plan
    # per user originated by this method. But there is no validation of uniqueness in
    # the DB.

    plan = await DbPlan.prisma().find_unique(where={"id": plan_id})
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found in user storage")

    if plan.is_favorite == favorite:
        # nothing to be done
        return await PlanView.from_db(plan)

    await DbPlan.prisma().query_raw("BEGIN")
    await DbPlan.prisma().query_raw(
        """
        UPDATE "Plan" SET is_favorite = FALSE
            WHERE user_rut = $1
        """,
        user.rut,
    )
    await DbPlan.prisma().query_raw(
        """
        UPDATE "Plan" SET is_favorite = $1
            WHERE id = $2
        """,
        favorite,
        plan_id,
    )
    await DbPlan.prisma().query_raw("COMMIT")

    updated_plan = await DbPlan.prisma().find_unique(where={"id": plan_id})

    # Must be true because access was authorized
    assert updated_plan is not None

    return await PlanView.from_db(updated_plan)


async def remove_plan(
    user: UserKey,
    plan_id: str,
    mod_access: bool = False,
) -> PlanView:
    await authorize_plan_access(user, plan_id, mod_access)

    deleted_plan = await DbPlan.prisma().delete(where={"id": plan_id})
    # Must be true because access was authorized
    assert deleted_plan is not None

    return await PlanView.from_db(deleted_plan)
