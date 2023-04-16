from .curriculum.diagnose import diagnose_curriculum
from .courses.validate import CourseInstance, PlanContext, is_satisfied, sanitize_plan
from ..courseinfo import CourseInfo, course_info
from ...sync import get_curriculum
from .diagnostic import ValidationResult
from ..plan import PseudoCourse, ValidatablePlan


async def diagnose_plan(plan: ValidatablePlan) -> ValidationResult:
    courseinfo = await course_info()
    curriculum = await get_curriculum(plan.curriculum)
    out = ValidationResult(diagnostics=[], course_superblocks={})

    # Ensure all courses are known
    plan = sanitize_plan(courseinfo, out, plan)

    # Ensure course requirements are met
    course_ctx = PlanContext(courseinfo, plan)
    course_ctx.validate(out)

    # Ensure the given curriculum is fulfilled
    diagnose_curriculum(courseinfo, curriculum, plan, out)

    return out


async def diagnose_plan_skip_curriculum(plan: ValidatablePlan) -> ValidationResult:
    courseinfo = await course_info()
    out = ValidationResult(diagnostics=[], course_superblocks={})

    course_ctx = PlanContext(courseinfo, plan)
    course_ctx.validate(out)

    return out


def quick_validate_dependencies(
    courseinfo: CourseInfo,
    plan: ValidatablePlan,
    semester: int,
    course: PseudoCourse,
) -> bool:
    assert courseinfo.try_course(course.code)
    course_ctx = PlanContext(courseinfo, plan)
    return is_satisfied(
        course_ctx,
        CourseInstance(course, semester),
        courseinfo.course(course.code).deps,
    )
