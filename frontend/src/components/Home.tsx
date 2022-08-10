import { FC, useState, useEffect, MouseEvent } from 'react';
import { useParams, useNavigate, useSearchParams, Outlet } from 'react-router-dom';
import StarRatingComponent from 'react-star-rating-component';
import { getCategories, getQuestions, TQuestion, deleteQuestion, addOrUpdateRating, deleteCategory } from '../utils/fetchDataUtils';
import { TCategory } from '../utils/fetchDataUtils';
import Pagination from './Pagination';


// clickable category link
const CategoryLink = ({ category, currentCategory }: { category: TCategory, currentCategory: number }) => {
  const navigate = useNavigate()

  const DeleteCategory = (e: MouseEvent<HTMLSpanElement>) => {
    e.preventDefault()
    deleteCategory(category.id!)
    .then((res) => {
      alert("sucess")
      navigate('/categories')
    })
  }

  return (
    <div className={`flex ${category.ownership ? 'justify-between' : 'justify-start'}`}>
      <li onClick={(e) => {
        e.preventDefault()
        navigate('/categories/' + category.id)
      }}
        key={category.id} className={`list-none hover:cursor-pointer pl-2 text-center md:text-left font-mono ${currentCategory === category.id ? 'text-blue-500' : ''}`}> {category.type}
      </li>
      {category.ownership ? <span onClick={DeleteCategory} className='text-red-600 hover:cursor-pointer font-bold'>X</span> : ''}
    </div>

  )
}


// question cards
const QuestionCard = ({ question, removeQuestion }: { question: TQuestion, removeQuestion: Function }) => {
  const [answerVisiblity, setAnswerVisibilty] = useState(false)
  const [mediumRating, setMediumRating] = useState<number>(1)
  const [individualRating, setIndividualRating] = useState<number>()

  useEffect(() => {
    setMediumRating(question.avg_rating!)
    question.rating ? setIndividualRating(question.rating) : setIndividualRating(0)
  }, [])

  const DeleteQuestion = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    if (window.confirm("Are you sure you want to delete this question?")) {
      deleteQuestion(question.id!)
        .then((res) => {
          alert("successfully deleted")
          removeQuestion(question.id)
        })
        .catch(() => {
          alert("unseccussful delete!")
        })
    }
  }

  const sendNewRating = (prev: number, next: number) => {
    addOrUpdateRating(question.id!, next)
      .then((res) => {
        alert('Updated')
        setIndividualRating(next)
        setMediumRating(res.medium)
      })
      .catch(() => {
        setIndividualRating(prev)
      })
  }

  return (
    <div className='border-purple-600 border-[3px] w-[90%] mb-1 rounded p-1 mx-auto relative'>
      <p className='inline-block bg-green-400 h-7 px-1 w-fit absolute top-0 right-0 font-medium'>{mediumRating} ⭐</p>
      <p className='text-gray-500'>question:</p>
      {question.question}
      <p className='text-gray-500'>difficulty: <span className='font-bold text-black'>{question.difficulty}</span></p>

      <button onClick={() => setAnswerVisibilty(!answerVisiblity)} className='bg-blue-600 hover:bg-blue-500 text-white font-bold p-2 rounded'>{answerVisiblity ? 'Hide' : 'Show'} Answer  <span className={`text-gray-900 font-bold ${answerVisiblity ? 'visible' : 'hidden'}`}>{question.answer}</span></button>

      {question.ownership !== 0 ? <button onClick={DeleteQuestion} className='inline-block bg-red-500 p-2 w-fit absolute bottom-0 right-0 text-white font-medium'>Delete</button> : ''}
      <div className='flex justify-center text-2xl'>
        <StarRatingComponent
          name="rating"
          starCount={5}
          value={individualRating!}
          onStarClick={(prevValue, nextValue) => {
            setIndividualRating(nextValue)
            sendNewRating(nextValue, prevValue)
          }}
        />
      </div>
    </div>
  )
}


export const QuestionsDisplay = () => {
  const [questions, setQuestions] = useState<TQuestion[]>([])
  const [pagesCount, setPagesCount] = useState(0)
  const [searchParams] = useSearchParams();

  let params = useParams();

  const removeQuestion = (givenId: number) => {
    setQuestions(questions.filter(el => el.id !== givenId))
  }

  useEffect(() => {
    params.categoryid ? getQuestions(parseInt(params.categoryid!), parseInt(searchParams.get('page')!))
      .then(res => {
        setQuestions(res.questions)
        setPagesCount(res.pagesCount)
      }).catch(err => {
        setQuestions([])
      })
      : null;
  }, [searchParams, params])

  return (
    <>
      {questions.length === 0 ? <div className='flex items-center justify-center'><span>No questions available in this category</span></div> : params.categoryid ? questions.map(el => <QuestionCard removeQuestion={removeQuestion} question={el} key={el.id} />) : <div className='flex items-center justify-center'><span>Choose a category</span></div>}

      <Pagination count={pagesCount} currentCategory={parseInt(params.categoryid!)} />
    </>
  )
}

const Home: FC = () => {
  const [categories, setCategories] = useState<TCategory[]>([])
  const [searchCategory, setSearchCategory] = useState('')

  let params = useParams();

  useEffect(() => {

    getCategories()
      .then(res => {
        setCategories(res)
      }).catch(err => {
        console.log(err);
      })

  }, [])

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchCategory(e.currentTarget.value)
  }


  return (
    <div className="h-fit flex flex-col md:flex-row">
      <div className="w-full md:w-[30%] mt-10 md:mt-0 p-2">
        <h3 className='text-center text-blue-600 text-lg mb-3 font-bold'>Categories</h3>
        {categories.filter(el => el.type.toLowerCase().includes(searchCategory.toLocaleLowerCase())).map((el) => <CategoryLink key={el.id} category={el} currentCategory={parseInt(params.categoryid!)} />)}

        <div className='flex flex-col items-center'>
          <p className='text-slate-700 pt-2'>search category:</p>
          <input type='text' value={searchCategory} onChange={handleSearch} />
        </div>
      </div>

      <div className="w-full md:w-[70%] mt-10 md:mt-0 border-l-2 border-black border-l-1 p-2 ">
        <h3 className='text-center text-pink-600 text-lg mb-3 font-bold'>Questions </h3>
        {params.categoryid ? <Outlet /> : <p className='text-center text-gray-600'>please select a category</p>}
      </div>
    </div>
  )
}

export default Home