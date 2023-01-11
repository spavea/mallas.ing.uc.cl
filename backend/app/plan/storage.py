from fastapi import HTTPException
from ..database import prisma
from prisma.types import (
    PlanCreateInput,
    PlanSemesterCreateInput,
    PlanClassCreateInput,
)
from ..plan.plan import ValidatablePlan, Level


async def store_plan(plan_name: str, user_rut: str, plan: ValidatablePlan):
    # TODO: set max 50 plans per user

    stored_plan = await prisma.plan.create(
        PlanCreateInput(
            name=plan_name,
            user_rut=user_rut,
            next_semester=plan.next_semester,
            level=plan.level,
            school=plan.school,
            program=plan.program,
            career=plan.career,
        )
    )

    for i, sem in enumerate(plan.classes):
        stored_semester = await prisma.plansemester.create(
            PlanSemesterCreateInput(plan_id=stored_plan.id, number=i + 1)
        )
        for cls in sem:
            await prisma.planclass.create(
                PlanClassCreateInput(semester_id=stored_semester.id, class_code=cls)
            )

    return stored_plan


async def get_plan_details(user_rut: str, plan_id: str):
    plan = (
        await prisma.query_raw(
            """
        SELECT * FROM "Plan"
        WHERE id = $1
        LIMIT 1
        """,
            plan_id,
        )
    )[0]

    if user_rut != plan["user_rut"]:
        raise HTTPException(status_code=404, detail="Plan not found in user storage")

    return await translate_plan_model(plan)


async def get_user_plans(user_rut: str):
    results = await prisma.query_raw(
        """
        SELECT * FROM "Plan"
        WHERE user_rut = $1
        LIMIT 50
        """,
        user_rut,
    )

    return [results[i] for i in range(len(results))]


async def modify_validatable_plan(
    user_rut: str, plan_id: str, new_plan: ValidatablePlan
):
    user_plans = await prisma.plan.find_many(where={"user_rut": user_rut})
    if plan_id not in [p.id for p in user_plans]:
        raise HTTPException(status_code=404, detail="Plan not found in user storage")

    updated_plan = await prisma.plan.update(
        where={
            "id": plan_id,
        },
        data={
            "next_semester": new_plan.next_semester,
            "level": new_plan.level,
            "school": new_plan.school,
            "program": new_plan.program,
            "career": new_plan.career,
        },
    )

    # TODO: use PlanSemesterUpdateManyWithoutRelationsInput for nested relations update
    # instead of the following inefficient algorithm

    # 1. remove old classes
    old_semesters = await prisma.plansemester.find_many(where={"plan_id": plan_id})

    for old_sem in old_semesters:
        classes = await prisma.planclass.find_many(where={"semester_id": old_sem.id})
        for cls in classes:
            await prisma.planclass.delete(where={"id": cls.id})
        await prisma.plansemester.delete(where={"id": old_sem.id})

    # 2. create new classes
    for i, new_sem in enumerate(new_plan.classes):
        stored_semester = await prisma.plansemester.create(
            PlanSemesterCreateInput(plan_id=plan_id, number=i + 1)
        )
        for cls in new_sem:
            await prisma.planclass.create(
                PlanClassCreateInput(semester_id=stored_semester.id, class_code=cls)
            )

    return updated_plan


async def modify_plan_name(user_rut: str, plan_id: str, new_name: str):
    user_plans = await prisma.plan.find_many(where={"user_rut": user_rut})
    if plan_id not in [p.id for p in user_plans]:
        raise HTTPException(status_code=404, detail="Plan not found in user storage")

    updated_plan = await prisma.plan.update(
        where={
            "id": plan_id,
        },
        data={
            "name": new_name,
        },
    )

    return updated_plan


async def remove_plan(user_rut: str, plan_id: str):
    user_plans = await prisma.plan.find_many(where={"user_rut": user_rut})
    if plan_id not in [p.id for p in user_plans]:
        raise HTTPException(status_code=404, detail="Plan not found in user storage")

    deleted_plan = await prisma.plan.delete(
        where={
            "id": plan_id,
        }
    )

    return deleted_plan


async def translate_plan_model(plan: dict[str, str | int]):

    semesters = await prisma.query_raw(
        """
            SELECT * FROM "PlanSemester"
            WHERE plan_id = $1
            """,
        plan["id"],
    )

    plan_classes: list[list[str]] = []
    for s in semesters:
        plan_class = await prisma.query_raw(
            """
                SELECT class_code FROM "PlanClass"
                WHERE semester_id = $1
                """,
            s["id"],
        )
        plan_class_stripped = [p["class_code"] for p in plan_class]

        plan_classes.append(plan_class_stripped)

    return {
        "id": plan["id"],
        "created_at": plan["created_at"],
        "updated_at": plan["updated_at"],
        "name": plan["name"],
        "plan": ValidatablePlan(
            classes=plan_classes,
            next_semester=int(plan["next_semester"]),
            level=Level(plan["level"]),
            school=str(plan["school"]),
            program=str(plan["program"]),
            career=str(plan["career"]),
        ),
    }
