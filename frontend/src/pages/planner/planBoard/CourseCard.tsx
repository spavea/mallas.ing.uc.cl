import { memo, ReactNode, useRef, Fragment } from 'react'
import { useDrag, useDrop } from 'react-dnd'
import editWhiteIcon from '../../../assets/editWhite.svg'
import editBlackIcon from '../../../assets/editBlack.svg'
import { useAuth } from '../../../contexts/auth.context'
import deepEqual from 'fast-deep-equal'

interface CourseCardProps {
  semester: number
  index: number
  cardData: { name: string, code: string, index: number, semester: number, credits?: number, is_concrete?: boolean }
  isDragging: Function
  moveCourse: Function
  remCourse: Function
  courseBlock: string
  openSelector: Function
  hasEquivalence?: boolean
  hasError: boolean
  hasWarning: boolean
}
interface CardProps {
  semester: number
  index: number
  cardData: { name: string, code: string, index: number, semester: number, credits?: number, is_concrete?: boolean }
  remCourse: Function
  courseBlock: string
  openSelector: Function
  hasEquivalence?: boolean
  hasError: boolean
  hasWarning: boolean
  isPassed: boolean
}

interface ConditionalWrapperProps {
  condition: boolean
  wrapper: Function
  children: ReactNode
}

const BlockInitials = (courseBlock: string): string => {
  switch (courseBlock) {
    case 'Ciencias':
      return 'PC'
    case 'Base':
      return 'PC'
    case 'Formacion':
      return 'FG'
    case 'Major':
      return 'M'
    case 'Minor':
      return 'm'
    case 'Ingeniero':
      return 'T'
  }
  return ''
}

const ConditionalWrapper = ({ condition, wrapper, children }: ConditionalWrapperProps): JSX.Element => {
  return (
    condition ? wrapper(children) : children
  )
}

const CourseCard = ({ semester, index, cardData, isDragging, moveCourse, remCourse, courseBlock, openSelector, hasEquivalence, hasError, hasWarning }: CourseCardProps): JSX.Element => {
  const ref = useRef(null)
  const authState = useAuth()

  const conditionPassed = authState?.passed?.[cardData.semester]?.find(o => o.code === cardData.code) !== undefined

  const [collected = { isDragging: false }, drag] = useDrag(() => ({
    type: 'card',
    item: () => {
      isDragging(true)
      return cardData
    },
    end () {
      isDragging(false)
    },
    collect (monitor) {
      return { isDragging: monitor.isDragging() }
    }
  }))
  const [dropProps, drop] = useDrop(() => ({
    accept: 'card',
    drop (course: { name: string, code: string, index: number, semester: number, credits?: number, is_concrete?: boolean }) {
      moveCourse({ semester: course.semester, index: course.index }, { semester, index })
      return course
    },
    collect: monitor => ({
      isOver: monitor.isOver()
    })
  }))

  if (!conditionPassed) {
    drag(drop(ref))
  }

  return (
    <Fragment>
      <div ref={ref} draggable={true} className={`px-2 ${!collected.isDragging ? 'pb-3' : ''} ${conditionPassed ? 'cursor-not-allowed opacity-50' : 'cursor-grab'} `}>
        {!collected.isDragging && <Fragment>{dropProps.isOver
          ? <div className={'card bg-place-holder'} />
          : <ConditionalWrapper condition={cardData.is_concrete !== true && courseBlock != null} wrapper={(children: ReactNode) => <button className='w-full' onClick={() => openSelector()}>{children}</button>}>
              <Card
                semester={semester}
                index={index}
                courseBlock={courseBlock}
                cardData={cardData}
                hasEquivalence={hasEquivalence}
                openSelector={openSelector}
                remCourse={remCourse}
                hasWarning={hasWarning}
                hasError={hasError}
                isPassed={conditionPassed}
              />
            </ConditionalWrapper>
          }
        </Fragment>}
      </div>
      {!collected.isDragging && dropProps.isOver && <div className={'px-2 pb-3'}>
      <Card
        semester={semester}
        index={index}
        courseBlock={courseBlock}
        cardData={cardData}
        hasEquivalence={hasEquivalence}
        openSelector={openSelector}
        remCourse={remCourse}
        hasWarning={hasWarning}
        hasError={hasError}
        isPassed={conditionPassed}
      />
      </div>
      }
    </Fragment>
  )
}

const Card = memo(function _Card ({ semester, index, courseBlock, cardData, hasEquivalence, openSelector, remCourse, hasWarning, hasError, isPassed }: CardProps): JSX.Element {
  const blockId = BlockInitials(courseBlock)
  const editIcon = (blockId === 'FG') ? editWhiteIcon : editBlackIcon

  // Turns out animations are a big source of lag
  const allowAnimations = false && blockId !== 'FG'

  return (
    <div className={`card group bg-block-${blockId} ${blockId === 'FG' ? 'text-white' : ''} ${cardData.is_concrete !== true && allowAnimations ? 'animated' : ''}`}>
      { hasEquivalence === true && (cardData.is_concrete === true
        ? <button onClick={() => openSelector()}><img className='opacity-60 absolute w-3 top-2 left-2' src={editIcon} alt="Seleccionar Curso" /></button>
        : <img className='opacity-60 absolute w-3 top-2 left-2' src={editIcon} alt="Seleccionar Curso" />
      )}
      {blockId === ''
        ? isPassed ? null : <button className='absolute top-0 right-2 hidden group-hover:inline' onClick={() => remCourse(semester, index)}>x</button>
        : <div className='absolute top-2 right-2 text-[0.6rem] opacity-75'>{blockId}</div>
      }
      <div className='flex items-center justify-center text-center flex-col'>
        <div className='text-xs line-clamp-2'>{cardData.name}</div>
        <div className='text-[0.6rem] opacity-75'>{cardData.is_concrete !== true ? 'Seleccionar Curso' : cardData.code}</div>
      </div>
      <div className='absolute bottom-2 left-2 text-[0.5rem] opacity-75'>{cardData.credits} créd.</div>
      {hasError && <span className="flex absolute h-3 w-3 top-0 right-0 -mt-1 -mr-1">
        <span className={`${allowAnimations ? 'animate-ping' : ''} absolute inline-flex h-full w-full rounded-full bg-red-300 opacity-90`}></span>
        <span className="relative inline-flex rounded-full h-3 w-3 bg-red-400"></span>
      </span> }
      {!hasError && hasWarning && <span className="flex absolute h-3 w-3 top-0 right-0 -mt-1 -mr-1">
        <span className={`${allowAnimations ? 'animate-ping' : ''} absolute inline-flex h-full w-full rounded-full bg-yellow-300 opacity-90`}></span>
        <span className="relative inline-flex rounded-full h-3 w-3 bg-yellow-400"></span>
      </span> }
  </div>
  )
})

export default memo(CourseCard, deepEqual)
