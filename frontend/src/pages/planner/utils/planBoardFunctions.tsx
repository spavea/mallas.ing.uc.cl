import { type CourseId, type CoursePos, type PseudoCourseId } from './Types'
import { type ValidatablePlan } from '../../../client'

export const getCoursePos = (prevCourses: PseudoCourseId[][], courseId: CourseId): CoursePos | null => {
  const positions: CoursePos[] = []

  prevCourses.forEach((sublist, semester) => {
    sublist.forEach((value, index) => {
      if (value.code === courseId.code) {
        positions.push({ semester, index })
      }
    })
  })
  if (positions.length <= courseId.instance || courseId.instance < 0) {
    return null
  }

  return positions[courseId.instance]
}

export const validateCourseMovement = (prev: ValidatablePlan, drag: CoursePos, drop: CoursePos): string | null => {
  const dragCourse = prev.classes[drag.semester][drag.index]

  if (
    dragCourse.is_concrete === true &&
      drop.semester !== drag.semester &&
      drop.semester < prev.classes.length &&
      prev.classes[drop.semester].map(course => course.code).includes(dragCourse.code)
  ) {
    return 'No se puede tener dos cursos iguales en un mismo semestre'
  }

  return null
}

export const updateClassesState = (prev: ValidatablePlan, drag: CoursePos, drop: CoursePos): ValidatablePlan => {
  const newClasses = [...prev.classes]
  const dragSemester = [...newClasses[drag.semester]]

  while (drop.semester >= newClasses.length) {
    newClasses.push([])
  }
  const dropSemester = [...newClasses[drop.semester]]
  const dragCourse = { ...dragSemester[drag.index] }
  const dropIndex = drop.index !== -1 ? drop.index : dropSemester.length
  if (drop.semester === drag.semester) {
    if (dropIndex < drag.index) {
      dragSemester.splice(dropIndex, 0, dragCourse)
      dragSemester.splice(drag.index + 1, 1)
    } else {
      dragSemester.splice(drag.index, 1)
      dragSemester.splice(dropIndex, 0, dragCourse)
    }
  } else {
    dropSemester.splice(dropIndex, 0, dragCourse)
    dragSemester.splice(drag.index, 1)
    newClasses[drop.semester] = dropSemester
  }

  newClasses[drag.semester] = dragSemester

  while (newClasses[newClasses.length - 1].length === 0) {
    newClasses.pop()
  }

  return { ...prev, classes: newClasses }
}
