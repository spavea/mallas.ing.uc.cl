import { Fragment, memo } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { Major, Minor, Title, CurriculumSpec } from '../../client'
import { CurriculumData } from './Planner'

interface CurriculumSelectorProps {
  planName: String
  curriculumData: CurriculumData | null
  curriculumSpec: CurriculumSpec | { cyear: null, major: null, minor: null, title: null }
  selectMajor: Function
  selectMinor: Function
  selectTitle: Function
}
interface SelectorProps {
  data: { [code: string]: Major | Minor | Title }
  value: string | null | undefined
  onChange: (value: string) => void
}

const Selector = memo(function _Selector ({
  data,
  value,
  onChange
}: SelectorProps): JSX.Element {
  return (
    <Listbox value={value !== undefined && value !== null ? data[value] : {}} onChange={onChange}>
      <Listbox.Button className="selectorButton">
        <span className="inline truncate">
          {value !== undefined && value !== null ? `${data[value]?.name} (${value})` : 'Por elegir'}
        </span>
        <svg
          className="inline"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          width="24"
          height="24"
        >
          <path fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M7 10l5 5 5-5"/>
        </svg>
      </Listbox.Button>
      <Transition
        as={Fragment}
        leave="transition ease-in duration-100"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
      >
        <Listbox.Options className="curriculumOptions" style={{ zIndex: 1 }}>
          {Object.keys(data).map((key) => (
            <Listbox.Option
              className={({ active }) =>
                `curriculumOption ${active ? 'bg-place-holder text-amber-800' : 'text-gray-900'}`
              }
              key={key}
              value={data[key]}
            >
              {({ selected }) => (
                <>
                  <span
                    className={`block truncate ${selected ? 'font-medium text-black' : 'font-normal'}`}
                  >
                    {data[key].name} ({key})
                  </span>
                  {selected
                    ? (
                    <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-800">*</span>
                      )
                    : null}
                </>
              )}
            </Listbox.Option>
          ))}
        </Listbox.Options>
      </Transition>
    </Listbox>
  )
})

/**
 * The selector of major, minor and tittle.
 */
const CurriculumSelector = memo(function CurriculumSelector ({
  planName,
  curriculumData,
  curriculumSpec,
  selectMajor,
  selectMinor,
  selectTitle
}: CurriculumSelectorProps): JSX.Element {
  return (
      <ul className={'curriculumSelector'}>
        <li className={'selectorElement'}>
          <div className={'selectorName'}>Major:</div>
          {curriculumData != null
            ? <Selector
              data={curriculumData.majors}
              value={curriculumSpec.major}
              onChange={(t) => selectMajor(t)}
            />
            : <svg
              className="inline"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="24"
              height="24"
            >
              <path fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M7 10l5 5 5-5"/>
            </svg>
          }
        </li>
        <li className={'selectorElement'}>
          <div className={'selectorName'}>Minor:</div>
          {curriculumData != null
            ? <Selector
              data={curriculumData.minors}
              value={curriculumSpec.minor}
              onChange={(t) => selectMinor(t)}
            />
            : <svg
                className="inline"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="24"
                height="24"
              >
              <path fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M7 10l5 5 5-5"/>
            </svg>
          }
        </li>
        <li className={'selectorElement'}>
          <div className={'selectorName'}>Titulo:</div>
          {curriculumData != null &&
            <Selector
              data={curriculumData.titles}
              value={curriculumSpec.title}
              onChange={(t) => selectTitle(t)}
            />
          }
        </li>
        {planName !== '' && <li className={'inline text-md ml-5 font-semibold'}><div className={'text-sm inline mr-1 font-normal'}>Plan:</div> {planName}</li>}
      </ul>
  )
})

export default CurriculumSelector