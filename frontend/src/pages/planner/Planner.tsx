import { Spinner } from '../../components/Spinner'
import ErrorTray from './ErrorTray'
import PlanBoard from './planBoard/PlanBoard'
import ControlTopBar from './ControlTopBar'
import CourseSelectorDialog from './dialogs/CourseSelectorDialog'
import LegendModal from './dialogs/LegendModal'
import SavePlanModal from './dialogs/SavePlanModal'
import CurriculumSelector from './CurriculumSelector'
import AlertModal from '../../components/AlertModal'
import { Navigate, useParams } from '@tanstack/react-router'
import { useState, useEffect, useRef, useCallback } from 'react'
import { type CourseDetails, type Major, DefaultService, type ValidatablePlan, type EquivDetails, type EquivalenceId, type ValidationResult, type PlanView, type CancelablePromise, type ClassId, type CurriculumSpec } from '../../client'
import { type PseudoCourseDetail, type PseudoCourseId, type CurriculumData, type ModalData, isCourseRequirementErr, type Cyear, type PossibleBlocksList } from './utils/Types'
import { validateCourseMovement, updateClassesState, locateClassInPlan } from './utils/PlanBoardFunctions'
import { useAuth } from '../../contexts/auth.context'
import { toast } from 'react-toastify'
import DebugGraph from '../../components/DebugGraph'
import deepEqual from 'fast-deep-equal'
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { collectRequirements, handleErrors, PlannerStatus } from './utils/utils'
import { updateCurriculum, isMinorValid, isMajorValid, loadCurriculumsData } from './utils/CurriculumUtils'
import ReceivePaste from './utils/ReceivePaste'
import ModBanner from './ModBanner'

/**
 * The main planner app. Contains the drag-n-drop main PlanBoard, the error tray and whatnot.
 */
const Planner = (): JSX.Element => {
  const [planName, setPlanName] = useState<string>('')
  const [planID, setPlanID] = useState<string | undefined>(useParams()?.plannerId)
  const [validatablePlan, setValidatablePlan] = useState<ValidatablePlan | null >(null)
  const [curriculumData, setCurriculumData] = useState<CurriculumData | null>(null)
  const [modalData, setModalData] = useState<ModalData>()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLegendModalOpen, setIsLegendModalOpen] = useState(false)
  const [isSavePlanModalOpen, setIsSavePlanModalOpen] = useState(false)
  const [plannerStatus, setPlannerStatus] = useState<PlannerStatus>(PlannerStatus.LOADING)
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [popUpAlert, setPopUpAlert] = useState<{ title: string, major?: string, year?: Cyear, deleteMajor: boolean, desc: string, isOpen: boolean }>({ title: '', major: '', deleteMajor: false, desc: '', isOpen: false })
  const [, setPossibleBlocksList] = useState<PossibleBlocksList>({}) // TODO: Use the possibleBlocksList

  const previousCurriculum = useRef<{ major: string | undefined, minor: string | undefined, title: string | undefined, cyear?: Cyear }>({ major: '', minor: '', title: '' })
  const previousClasses = useRef<PseudoCourseId[][]>([[]])

  // NOTE: Course rendering kind of depends on course details, but in practice courses should always have their course details available before their first render
  const courseDetails = useRef<Record<string, PseudoCourseDetail>>({})

  const [, setValidationPromise] = useState<CancelablePromise<any> | null>(null)
  const impersonateRut = useParams()?.userRut
  const authState = useAuth()

  const addCourseDetails = useCallback((details: PseudoCourseDetail[]) => {
    for (const detail of details) {
      courseDetails.current[detail.code] = detail
    }
  }, [courseDetails])

  const getCourseDetails = useCallback(async (courses: PseudoCourseId[], fetchAll: CurriculumSpec | undefined = undefined): Promise<void> => {
    const pseudocourseCodes = new Set<string>()
    for (const courseid of courses) {
      const code = ('failed' in courseid ? courseid.failed : null) ?? courseid.code
      if (!(code in courseDetails.current)) {
        pseudocourseCodes.add(code)
      }
    }
    if (pseudocourseCodes.size === 0 && fetchAll == null) return
    console.log(`getting ${pseudocourseCodes.size} course details...`)
    try {
      const newDetails = await DefaultService.getPseudocourseDetails({ codes: Array.from(pseudocourseCodes), plan: fetchAll })
      if (fetchAll != null) {
        // Process all equivalences
        const blocksList: Record<string, EquivDetails[]> = {}
        for (const detail of newDetails) {
          if ('courses' in detail) {
            for (const course of detail.courses) {
              if (!(course in blocksList)) blocksList[course] = []
              blocksList[course].push(detail)
            }
          }
        }
        setPossibleBlocksList(blocksList)
      }
      addCourseDetails(newDetails)
    } catch (err) {
      handleErrors(err, setPlannerStatus, setError)
    }
  }, [addCourseDetails])

  const validate = useCallback(async (validatablePlan: ValidatablePlan): Promise<void> => {
    try {
      if (validatablePlan.classes.flat().length === 0) {
        setValidationPromise(prev => {
          if (prev != null) {
            prev.cancel()
            return null
          }
          return prev
        })
        previousClasses.current = validatablePlan.classes
        previousCurriculum.current = {
          major: validatablePlan.curriculum.major,
          minor: validatablePlan.curriculum.minor,
          title: validatablePlan.curriculum.title,
          cyear: validatablePlan.curriculum.cyear
        }
        setPlannerStatus(PlannerStatus.READY)
        return
      }
      const promise = authState?.user == null
        ? DefaultService.validateGuestPlan(validatablePlan)
        : (authState?.isMod === true && impersonateRut != null)
            ? DefaultService.validatePlanForAnyUser(impersonateRut, validatablePlan)
            : DefaultService.validatePlanForUser(validatablePlan)
      setValidationPromise(prev => {
        if (prev != null) {
          prev.cancel()
        }
        return promise
      })
      const response = await promise
      setValidationPromise(null)
      previousCurriculum.current = {
        major: validatablePlan.curriculum.major,
        minor: validatablePlan.curriculum.minor,
        title: validatablePlan.curriculum.title,
        cyear: validatablePlan.curriculum.cyear
      }
      // Order diagnostics by putting errors first, then warnings.
      response.diagnostics.sort((a, b) => {
        if (a.is_err === b.is_err) {
          return 0
        } else if (a.is_err ?? true) {
          return -1
        } else {
          return 1
        }
      })
      const reqCourses = new Set<string>()
      for (const diag of response.diagnostics) {
        if (isCourseRequirementErr(diag)) {
          collectRequirements(diag.modernized_missing, reqCourses)
        }
      }
      if (reqCourses.size > 0) {
        await getCourseDetails(Array.from(reqCourses).map((code: string) => { return { code, isConcrete: true } }))
      }
      setValidationResult(prev => {
        // Validation often gives the same results after small changes
        // Avoid triggering changes if this happens
        if (deepEqual(prev, response)) return prev
        return response
      })
      setPlannerStatus(PlannerStatus.READY)
      previousClasses.current = validatablePlan.classes
    } catch (err) {
      handleErrors(err, setPlannerStatus, setError)
    }
  }, [authState?.isMod, impersonateRut, authState?.user, getCourseDetails])

  const savePlan = useCallback(async (planName: string): Promise<void> => {
    if (validatablePlan == null) {
      toast.error('No se ha generado un plan aun')
      return
    }
    if (planID !== null && planID !== undefined) {
      setPlannerStatus(PlannerStatus.VALIDATING)
      try {
        await DefaultService.updatePlan(planID, validatablePlan)
        toast.success('Plan actualizado exitosamente.')
      } catch (err) {
        handleErrors(err, setPlannerStatus, setError)
      }
    } else {
      if (planName == null || planName === '') return
      setPlannerStatus(PlannerStatus.VALIDATING)
      try {
        const res = await DefaultService.savePlan(planName, validatablePlan)
        setPlanID(res.id)
        setPlanName(res.name)
        toast.success('Plan guardado exitosamente')
      } catch (err) {
        handleErrors(err, setPlannerStatus, setError)
      }
    }
    setIsSavePlanModalOpen(false)
    setPlannerStatus(PlannerStatus.READY)
  }, [planID, validatablePlan])

  const openModalForExtraClass = useCallback((semIdx: number): void => {
    setModalData({
      equivalence: undefined,
      selector: true,
      semester: semIdx
    })
    setIsModalOpen(true)
  }, []) // addCourse should not depend on `validatablePlan`, so that memoing does its work

  const remCourse = useCallback((course: ClassId): void => {
    setValidatablePlan(prev => {
      if (prev === null) return null
      const remPos = locateClassInPlan(prev.classes, course)
      if (remPos == null) {
        toast.error('Index no encontrado')
        return prev
      }
      const newClases = [...prev.classes]
      const newClasesSem = [...prev.classes[remPos.semester]]
      newClasesSem.splice(remPos.index, 1)
      newClases[remPos.semester] = newClasesSem
      while (newClases[newClases.length - 1].length === 0) {
        newClases.pop()
      }
      return { ...prev, classes: newClases }
    })
  }, []) // remCourse should not depend on `validatablePlan`, so that memoing does its work

  const moveCourse = useCallback((drag: ClassId, drop: { semester: number, index: number }): void => {
    setValidatablePlan(prev => {
      if (prev === null) return prev
      const dragIndex = locateClassInPlan(prev.classes, drag)
      if (dragIndex == null) {
        toast.error('Index no encontrado')
        return prev
      }
      const validationError = validateCourseMovement(prev, dragIndex, drop)

      if (validationError !== null) {
        toast.error(validationError)
        return prev
      }
      return updateClassesState(prev, dragIndex, drop)
    })
  }, [])

  const initializePlan = useCallback(async (validatablePlan: ValidatablePlan) => {
    await Promise.all([
      getCourseDetails(validatablePlan.classes.flat(), validatablePlan.curriculum),
      loadCurriculumsData(validatablePlan.curriculum.cyear, setCurriculumData, validatablePlan.curriculum.major),
      validate(validatablePlan)
    ])
    setValidatablePlan(validatablePlan)
    console.log('data loaded')
  }, [getCourseDetails, validate])

  const getPlanById = useCallback(async (id: string): Promise<void> => {
    try {
      console.log('Getting Plan by Id...')
      let response: PlanView
      if (authState?.isMod === true) {
        response = await DefaultService.readAnyPlan(id)
      } else {
        response = await DefaultService.readPlan(id)
      }
      previousClasses.current = response.validatable_plan.classes
      previousCurriculum.current = {
        major: response.validatable_plan.curriculum.major,
        minor: response.validatable_plan.curriculum.minor,
        title: response.validatable_plan.curriculum.title,
        cyear: response.validatable_plan.curriculum.cyear
      }
      setPlanName(response.name)
      await initializePlan(response.validatable_plan)
    } catch (err) {
      handleErrors(err, setPlannerStatus, setError)
    }
  }, [authState?.isMod, initializePlan])

  const getDefaultPlan = useCallback(async (referenceValidatablePlan?: ValidatablePlan, truncateAt?: number): Promise<void> => {
    try {
      console.log('Getting Basic Plan...')
      let baseValidatablePlan
      if (referenceValidatablePlan === undefined || referenceValidatablePlan === null) {
        baseValidatablePlan = authState?.user == null
          ? await DefaultService.emptyGuestPlan()
          : (authState?.isMod === true && impersonateRut != null) ? await DefaultService.emptyPlanForAnyUser(impersonateRut) : await DefaultService.emptyPlanForUser()
      } else {
        baseValidatablePlan = { ...referenceValidatablePlan, classes: [...referenceValidatablePlan.classes] }
        truncateAt = truncateAt ?? (authState?.student?.next_semester ?? 0)
        baseValidatablePlan.classes.splice(truncateAt)
      }
      // truncate the validatablePlan to the last not empty semester
      while (baseValidatablePlan.classes.length > 0 && baseValidatablePlan.classes[baseValidatablePlan.classes.length - 1].length === 0) {
        baseValidatablePlan.classes.pop()
      }
      const response: ValidatablePlan = await DefaultService.generatePlan({
        passed: baseValidatablePlan,
        reference: referenceValidatablePlan ?? undefined
      })
      previousClasses.current = response.classes
      previousCurriculum.current = {
        major: response.curriculum.major,
        minor: response.curriculum.minor,
        title: response.curriculum.title,
        cyear: response.curriculum.cyear
      }
      await initializePlan(response)
    } catch (err) {
      handleErrors(err, setPlannerStatus, setError)
    }
  }, [authState?.student?.next_semester, impersonateRut, authState?.isMod, authState?.user, initializePlan])

  const fetchData = useCallback(async (): Promise<void> => {
    try {
      if (planID != null) {
        await getPlanById(planID)
      } else {
        await getDefaultPlan()
      }
    } catch (error) {
      setError('Hubo un error al cargar el planner')
      console.error(error)
      setPlannerStatus(PlannerStatus.ERROR)
    }
  }, [getDefaultPlan, getPlanById, planID])

  const loadNewPLan = useCallback(async (referenceValidatablePlan: ValidatablePlan): Promise<void> => {
    try {
      await getDefaultPlan(referenceValidatablePlan)
    } catch (error) {
      setError('Hubo un error al cargar el planner')
      console.error(error)
      setPlannerStatus(PlannerStatus.ERROR)
    }
  }, [getDefaultPlan])

  const openModal = useCallback(async (equivalence: EquivDetails | EquivalenceId, semester: number, index?: number): Promise<void> => {
    if ('courses' in equivalence) {
      setModalData({ equivalence, selector: false, semester, index })
    } else {
      const response = (
        courseDetails.current[equivalence.code] ??
        (await DefaultService.getPseudocourseDetails({ codes: [equivalence.code] }))[0]
      )
      if (!('courses' in response)) {
        throw new Error('expected equivalence details')
      }
      setModalData({ equivalence: response, selector: false, semester, index })
    }
    setIsModalOpen(true)
  }, [courseDetails])

  const closeModal = useCallback(async (selection?: CourseDetails): Promise<void> => {
    if (selection != null && modalData !== undefined) {
      addCourseDetails([selection])
      setValidatablePlan(prev => {
        if (prev === null) return prev
        const newValidatablePlan = { ...prev, classes: [...prev.classes] }
        while (newValidatablePlan.classes.length <= modalData.semester) {
          newValidatablePlan.classes.push([])
        }
        const index = modalData.index ?? newValidatablePlan.classes[modalData.semester].length
        const pastClass = newValidatablePlan.classes[modalData.semester][index]
        if (pastClass !== undefined && selection.code === pastClass.code) { setIsModalOpen(false); return prev }
        for (const existingCourse of newValidatablePlan.classes[modalData.semester].flat()) {
          if (existingCourse.code === selection.code) {
            toast.error(`${selection.name} ya se encuentra en este semestre, seleccione otro curso por favor`)
            return prev
          }
        }
        newValidatablePlan.classes[modalData.semester] = [...newValidatablePlan.classes[modalData.semester]]
        if (modalData.equivalence === undefined) {
          while (newValidatablePlan.classes.length <= modalData.semester) {
            newValidatablePlan.classes.push([])
          }
          newValidatablePlan.classes[modalData.semester][index] = {
            is_concrete: true,
            code: selection.code,
            equivalence: undefined
          }
        } else {
          const oldEquivalence = 'credits' in pastClass ? pastClass : pastClass.equivalence

          newValidatablePlan.classes[modalData.semester][index] = {
            is_concrete: true,
            code: selection.code,
            equivalence: oldEquivalence
          }
          if (oldEquivalence !== undefined && oldEquivalence.credits !== selection.credits) {
            if (oldEquivalence.credits > selection.credits) {
              newValidatablePlan.classes[modalData.semester].splice(index, 1,
                {
                  is_concrete: true,
                  code: selection.code,
                  equivalence: {
                    ...oldEquivalence,
                    credits: selection.credits
                  }
                },
                {
                  is_concrete: false,
                  code: oldEquivalence.code,
                  credits: oldEquivalence.credits - selection.credits
                }
              )
            } else {
              // handle when credis exced necesary
              // Partial solution: just consume anything we find
              const semester = newValidatablePlan.classes[modalData.semester]
              let extra = selection.credits - oldEquivalence.credits
              for (let i = semester.length; i-- > 0;) {
                const equiv = semester[i]
                if ('credits' in equiv && equiv.code === oldEquivalence.code) {
                  if (equiv.credits <= extra) {
                    // Consume this equivalence entirely
                    semester.splice(index, 1)
                    extra -= equiv.credits
                  } else {
                    // Consume part of this equivalence
                    equiv.credits -= extra
                    extra = 0
                  }
                }
              }

              // Increase the credits of the equivalence
              // We might not have found all the missing credits, but that's ok
              newValidatablePlan.classes[modalData.semester].splice(index, 1,
                {
                  is_concrete: true,
                  code: selection.code,
                  equivalence: {
                    ...oldEquivalence,
                    credits: selection.credits
                  }
                }
              )
            }
          }
        }
        setPlannerStatus(PlannerStatus.VALIDATING)
        setIsModalOpen(false)
        return newValidatablePlan
      })
    } else {
      setIsModalOpen(false)
    }
  }, [addCourseDetails, modalData])

  const openLegendModal = useCallback((): void => {
    setIsLegendModalOpen(true)
  }, [setIsLegendModalOpen])

  const closeLegendModal = useCallback((): void => {
    setIsLegendModalOpen(false)
  }, [setIsLegendModalOpen])

  const openSavePlanModal = useCallback(async (): Promise<void> => {
    if (planName == null || planName === '') {
      setIsSavePlanModalOpen(true)
    } else {
      await savePlan(planName)
    }
  }, [planName, savePlan])

  const closeSavePlanModal = useCallback((): void => {
    setIsSavePlanModalOpen(false)
  }, [])

  const reset = useCallback((): void => {
    setPlannerStatus(PlannerStatus.LOADING)
    setValidatablePlan(null)
  }, [])

  const selectYear = useCallback((cYear: Cyear, isMajorValid: boolean, isMinorValid: boolean): void => {
    setValidatablePlan((prev) => {
      if (prev == null || prev.curriculum.cyear === cYear) return prev
      const newCurriculum = { ...prev.curriculum, cyear: cYear }
      const newClasses = [...prev.classes]
      newClasses.splice(authState?.student?.next_semester ?? 0)
      if (!isMinorValid) {
        newCurriculum.minor = undefined
      }
      if (!isMajorValid) {
        newCurriculum.major = undefined
      }
      return { ...prev, classes: newClasses, curriculum: newCurriculum }
    })
  }, [setValidatablePlan, authState])

  const checkMinorForNewMajor = useCallback(async (major: Major): Promise<void> => {
    const isValidMinor = await isMinorValid(major.cyear, major.code, validatablePlan?.curriculum.minor)
    if (!isValidMinor) {
      setPopUpAlert({
        title: 'Minor incompatible',
        desc: 'Advertencia: La selección del nuevo major no es compatible con el minor actual. Continuar con esta selección requerirá eliminar el minor actual. ¿Desea continuar y eliminar su minor?',
        major: major.code,
        deleteMajor: false,
        isOpen: true
      })
    } else {
      setValidatablePlan(prev => {
        return updateCurriculum(prev, 'major', major.code, true)
      })
    }
  }, [validatablePlan?.curriculum, setPopUpAlert]) // this sensitivity list shouldn't contain frequently-changing attributes

  const handlePopUpAlert = useCallback(async (isCanceled: boolean): Promise<void> => {
    setPopUpAlert(prev => {
      if (!isCanceled) {
        if ('major' in prev) {
          setValidatablePlan(prevPlan => {
            return updateCurriculum(prevPlan, 'major', prev.major, false)
          })
        }
        if ('year' in prev && prev.year !== undefined) {
          if (prev.deleteMajor) {
            selectYear(prev.year, false, false)
          } else {
            selectYear(prev.year, true, false)
          }
        }
      }
      return { ...prev, isOpen: false }
    })
  }, [selectYear])

  const checkMajorAndMinorForNewYear = useCallback(async (cyear: Cyear): Promise<void> => {
    const isValidMajor = await isMajorValid(cyear, validatablePlan?.curriculum.major)
    if (!isValidMajor) {
      setPopUpAlert({
        title: 'Major incompatible',
        desc: 'Advertencia: La selección del nuevo año no es compatible con el major actual. Continuar con esta selección requerirá eliminar el major y minor actual. ¿Desea continuar y eliminar su minor?',
        year: cyear,
        deleteMajor: true,
        isOpen: true
      })
    } else {
      const isValidMinor = await isMinorValid(cyear, validatablePlan?.curriculum.major, validatablePlan?.curriculum.minor)
      if (!isValidMinor) {
        setPopUpAlert({
          title: 'Minor incompatible',
          desc: 'Advertencia: La selección del nuevo año no es compatible con el minor actual. Continuar con esta selección requerirá eliminar el minor actual. ¿Desea continuar y eliminar su minor?',
          year: cyear,
          deleteMajor: false,
          isOpen: true
        })
      } else {
        selectYear(cyear, true, true)
      }
    }
  }, [validatablePlan?.curriculum, setPopUpAlert, selectYear])

  const selectMinor = useCallback((minorCode: string | undefined): void => {
    setValidatablePlan(prev => {
      return updateCurriculum(prev, 'minor', minorCode, true)
    })
  }, []) // this sensitivity list shouldn't contain frequently-changing attributes

  const selectTitle = useCallback((titleCode: string | undefined): void => {
    setValidatablePlan(prev => {
      return updateCurriculum(prev, 'title', titleCode, true)
    })
  }, [])

  useEffect(() => {
    setPlannerStatus(PlannerStatus.LOADING)
  }, [])

  useEffect(() => {
    console.log(`planner status set to ${plannerStatus}`)
    if (plannerStatus === 'LOADING') {
      void fetchData()
    }
  }, [plannerStatus, fetchData])

  useEffect(() => {
    if (validatablePlan != null) {
      const { major, minor, title, cyear } = validatablePlan.curriculum
      const curriculumChanged =
          major !== previousCurriculum.current.major ||
          minor !== previousCurriculum.current.minor ||
          title !== previousCurriculum.current.title ||
          cyear !== previousCurriculum.current.cyear
      if (curriculumChanged) {
        setPlannerStatus(PlannerStatus.CHANGING_CURRICULUM)
        void loadNewPLan(validatablePlan)
      } else {
        setPlannerStatus(prev => {
          if (prev === PlannerStatus.LOADING) return prev
          return PlannerStatus.VALIDATING
        })
        validate(validatablePlan).catch(err => {
          handleErrors(err, setPlannerStatus, setError)
        })
      }
    }
  }, [validatablePlan, validate, loadNewPLan])

  if (impersonateRut !== authState?.student?.rut && impersonateRut !== undefined && authState?.isMod === true) {
    return <Navigate to="/mod/users"/>
  }
  return (
    <>
      {authState?.isMod === true &&
        <ModBanner/>
      }
      <div className={`w-full relative h-full flex flex-grow overflow-hidden flex-row ${(plannerStatus === 'LOADING') ? 'cursor-wait' : ''}`}>
        <DebugGraph validatablePlan={validatablePlan} />
        <ReceivePaste validatablePlan={validatablePlan} getDefaultPlan={getDefaultPlan} />
        <CourseSelectorDialog equivalence={modalData?.equivalence} open={isModalOpen} onClose={closeModal}/>
        <LegendModal open={isLegendModalOpen} onClose={closeLegendModal}/>
        <SavePlanModal isOpen={isSavePlanModalOpen} onClose={closeSavePlanModal} savePlan={savePlan}/>
        <AlertModal title={popUpAlert.title} isOpen={popUpAlert.isOpen} close={handlePopUpAlert}>{popUpAlert.desc}</AlertModal>
        {(plannerStatus === PlannerStatus.LOADING || plannerStatus === PlannerStatus.CHANGING_CURRICULUM) &&
          <div className="absolute w-screen h-full z-50 bg-white flex flex-col justify-center items-center">
            <Spinner message='Cargando planificación...' />
          </div>
        }

        {plannerStatus === 'ERROR'
          ? (<div className={'w-full h-full flex flex-col justify-center items-center'}>
              <p className={'text-2xl font-semibold mb-4'}>Error al cargar plan</p>
              <p className={'text-sm font-normal'}>{error}</p>
              <a href="https://github.com/open-source-uc/planner/issues?q=is%3Aopen+is%3Aissue+label%3Abug" className={'text-blue-700 underline text-sm'} rel="noreferrer" target="_blank">Reportar error</a>
            </div>)
          : <div className={'flex w-full p-3 pb-0'}>
              <div className={'flex flex-col overflow-auto flex-grow'}>
                <CurriculumSelector
                  planName={planName}
                  curriculumData={curriculumData}
                  curriculumSpec={validatablePlan?.curriculum ?? { cyear: null, major: null, minor: null, title: null }}
                  selectMajor={checkMinorForNewMajor}
                  selectMinor={selectMinor}
                  selectTitle={selectTitle}
                  selectYear={checkMajorAndMinorForNewYear}
                />
                <ControlTopBar
                  reset={reset}
                  openSavePlanModal={openSavePlanModal}
                  openLegendModal={openLegendModal}
                  isMod={authState?.isMod === true}
                />
                <DndProvider backend={HTML5Backend}>
                  <PlanBoard
                    classesGrid={validatablePlan?.classes ?? []}
                    validationResult={validationResult}
                    classesDetails={courseDetails.current}
                    moveCourse={moveCourse}
                    openModal={openModal}
                    authState={authState}
                    addCourse={openModalForExtraClass}
                    remCourse={remCourse}
                    />
                </DndProvider>
              </div>
            <ErrorTray
              setValidatablePlan={setValidatablePlan}
              getCourseDetails={getCourseDetails}
              diagnostics={validationResult?.diagnostics ?? []}
              validating={plannerStatus === 'VALIDATING'}
              courseDetails={courseDetails.current}
            />
          </div>
        }
      </div>
    </>
  )
}

export default Planner
