import axios from 'axios'
import { FC, FormEvent, useState } from 'react'


const AddQuestion: FC = () => {
  const [question, setQuestion] = useState()
  const [answer, setAnswer] = useState()
  const [difficulty, setDifficulty] = useState()
  const [category_id, setCategory] = useState()

  const addQuestion = (e: FormEvent) => {
    e.preventDefault()
    axios({
      method: "POST",
      url: `${import.meta.env.BASE_URL}/questions`,
      data: {
        question,
        answer,
        difficulty,
        category_id,
      }
    })
  }

  return (
    <div className='w-full h-full mx-auto'>
      <form onSubmit={addQuestion}></form>
    </div>
  )
}

export default AddQuestion