import { FC, useState, useEffect, MouseEvent } from 'react';
import { useParams, useNavigate, useSearchParams, Outlet } from 'react-router-dom';
import { getCategories, getCategoryQuestions, deleteCategory } from '../utils/fetchDataUtils';
import { TCategory } from '../utils/fetchDataUtils';
import useStore from '../zustandStore/store';
import Pagination from './Pagination';
import QuestionCard from './QuestionCard';


// clickable category link
const CategoryLink = ({ category, currentCategory }: { category: TCategory, currentCategory: number, setCategories: Function, categories: TCategory[] }) => {
  const navigate = useNavigate()
  const [categories, setCategories, user] = useStore(state => [state.categories, state.setCategories, state.user])

  const DeleteCategory = (e: MouseEvent<HTMLSpanElement>) => {
    e.preventDefault()
    if (window.confirm("Are you sure you want to delete this question?")) {
      deleteCategory(category.id!)
        .then((res) => {
          alert("sucess")
          navigate('/list/categories')
          setCategories([...categories.filter(cat => cat.id !== category.id)])
        })
    }

  }

  return (
    <div className={`flex ${category.ownership !== null ? 'justify-between' : 'justify-start'}`}>
      <li onClick={(e) => {
        e.preventDefault()
        navigate('/list/categories/' + category.id)
      }}
        key={category.id} className={`list-none hover:cursor-pointer pl-2 text-center md:text-left font-mono ${currentCategory === category.id ? 'text-blue-500' : ''}`}> {category.type}
      </li>
      {(category.ownership == 0 && user?.id == 0) || (category.ownership) ? <span onClick={DeleteCategory} className='text-red-600 hover:cursor-pointer font-bold'>X</span> : ''}
    </div>

  )
}




export const QuestionsDisplay = () => {
  const [questions, setQuestions] = useStore(state => [state.questions, state.setQuestions])
  const [pagesCount, setPagesCount] = useState(0)
  const [searchParams] = useSearchParams();

  let params = useParams();

  const removeQuestion = (givenId: number) => {
    setQuestions(questions.filter(el => el.id !== givenId))
  }

  useEffect(() => {
    params.categoryid ? getCategoryQuestions(parseInt(params.categoryid!), parseInt(searchParams.get('page')!))
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

      <Pagination count={pagesCount} url={`/list/categories/${parseInt(params.categoryid!)}`} />
    </>
  )
}

const Home: FC = () => {
  const [categories, setCategories] = useStore(state => [state.categories, state.setCategories])
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
        {categories.filter(el => el.type.toLowerCase().includes(searchCategory.toLocaleLowerCase())).map((el) => <CategoryLink key={el.id} category={el} currentCategory={parseInt(params.categoryid!)} setCategories={setCategories} categories={categories} />)}

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