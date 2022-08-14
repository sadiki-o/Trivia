import { MouseEvent, useEffect, useState } from "react"
import StarRatingComponent from "react-star-rating-component"
import { addOrUpdateRating, deleteQuestion, TQuestion } from "../utils/fetchDataUtils"
import useStore from "../zustandStore/store"

const QuestionCard = ({ question, removeQuestion }: { question: TQuestion, removeQuestion: Function }) => {
    const [answerVisiblity, setAnswerVisibilty] = useState(false)
    const [mediumRating, setMediumRating] = useState<number>(question.avg_rating!)
    const [individualRating, setIndividualRating] = useState<number>(question.rating ? question.rating : 0)
  
    const user = useStore(state => state.user)
  
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
        .catch((err) => {
          setIndividualRating(prev)
          console.log(err)        
        })
    }
  
    return (
      <div className='border-purple-600 border-[3px] w-[90%] mb-1 rounded p-1 mx-auto relative'>
        <p className='inline-block bg-green-400 h-7 px-1 w-fit absolute top-0 right-0 font-medium'>{mediumRating} ⭐</p>
        <p className='text-gray-500'>question:</p>
        {question.question}
        <p className='text-gray-500'>difficulty: <span className='font-bold text-black'>{question.difficulty}</span></p>
  
        <button onClick={() => setAnswerVisibilty(!answerVisiblity)} className='bg-blue-600 hover:bg-blue-500 text-white font-bold p-2 rounded'>{answerVisiblity ? 'Hide' : 'Show'} Answer  <span className={`text-gray-900 font-bold ${answerVisiblity ? 'visible' : 'hidden'}`}>{question.answer}</span></button>
  
        {question.ownership === user?.id ? <button onClick={DeleteQuestion} className='inline-block bg-red-500 p-2 w-fit absolute bottom-0 right-0 text-white font-medium'>Delete</button> : ''}
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

export default QuestionCard