import { FC, FormEvent, useState, useEffect } from 'react';
import { addCategory, addQuestion, getCategories, TCategory } from '../utils/fetchDataUtils';


const Add: FC = () => {
  const [categories, setCategories] = useState<TCategory[]>([])

  //questions
  const [question, setQuestion] = useState<string>('')
  const [answer, setAnswer] = useState<string>('')
  const [difficulty, setDifficulty] = useState<number>(1)
  const [category, setCategory] = useState<number>(1)

  //categories
  const [newCategory, setNewCategory] = useState<string>('')

  useEffect(() => {
    getCategories()
      .then(res => {
        setCategories(res)
      }).catch(err => {
        console.log(err);
      })
  }, [])

  const insertQuestion = (e: FormEvent) => {
    e.preventDefault()
    if (question && answer && difficulty && category) {
      addQuestion({
        question,
        answer,
        difficulty,
        category
      }).then((res) => {
        alert("Question successfully added ")
        setQuestion('')
        setAnswer('')
      }).catch(() => {
        alert("Question wasn't added ")
      })
    }

  }

  const insertCategory = (e: FormEvent) => {
    e.preventDefault()
    if (newCategory) {
      addCategory(newCategory).then((res) => {
        alert("Category successfully added ")
        setNewCategory('')
      }).catch(() => {
        alert("Category wasn't added ")
      })
    }
  }

  return (
    <div className='flex flex-col md:flex-row gap-2 p-6'>
      <form onSubmit={insertQuestion} className='bg-gray-100 p-4 rounded w-full'>
        <h1 className='text-cEnter font-bold mb-4 text-slate-500 text-xl'>Insert Questions</h1>
        <label className='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>Question : </label>
        <input onChange={(e) => setQuestion(e.currentTarget.value)} value={question} type="text" className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' placeholder='Enter your question' required /><br />

        <label className='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>Answer : </label>
        <input onChange={(e) => setAnswer(e.currentTarget.value)} value={answer} type="text" className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' placeholder='Enter your answer' required /><br />

        <label className='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>Difficulty : </label>
        <select onChange={(e) => setDifficulty(parseInt(e.currentTarget.value))} value={difficulty} className=' block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' required>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select><br />

        <label className='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>Category : </label>
        <select onChange={(e) => setCategory(parseInt(e.currentTarget.value))} value={category} className=' block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500 required:'>
          {categories.map(cat => <option key={cat.id} value={cat.id}>{cat.type}</option>)}
        </select><br />

        <input className='p-3 bg-blue-500 rounded block hover:cursor-pointer hover:bg-blue-300 font-bold text-white mx-auto' type="submit" value="Submit" />

      </form>

      <form onSubmit={insertCategory} className='p-4 rounded w-full bg-white h-fit'>
        <h1 className='text-cEnter font-bold mb-4 text-slate-500 text-xl'>Insert Category </h1>
        <label className='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>Name : </label>
        <input onChange={(e) => setNewCategory(e.currentTarget.value)} value={newCategory} type="text" className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' placeholder='Enter category name' required /><br />

        <input className='p-3 bg-green-500 rounded block hover:cursor-pointer hover:bg-green-300 font-bold text-white mx-auto' type="submit" value="Submit" />
      </form>
    </div>
  )
}

export default Add