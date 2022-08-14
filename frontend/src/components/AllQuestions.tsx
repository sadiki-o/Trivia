import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { getAllQuestions, searchQuestions } from "../utils/fetchDataUtils"
import useStore from "../zustandStore/store"
import Pagination from "./Pagination"
import QuestionCard from "./QuestionCard"

const AllQuestions = () => {
    const [questions, setQuestions, allQuestions, setAllQuestions] = useStore(state => [state.questions, state.setQuestions, state.allQuestions, state.setAllQuestions])
    const [pagesCount, setPagesCount] = useState<number>(0)
    const [searchParams] = useSearchParams();
    const [searchQuestion, setSearchQuestion] = useState('')

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuestion(e.currentTarget.value)

        searchQuestions(searchQuestion)
            .then(res => {
                setAllQuestions(res)
            })
    }

    const removeQuestion = (givenId: number) => {
        setAllQuestions(allQuestions.filter(el => el.id !== givenId))
        setQuestions(allQuestions.filter(el => el.id !== givenId))
    }

    useEffect(() => {
        getAllQuestions(parseInt(searchParams.get('page')!))
            .then(res => {
                setQuestions(res.questions)
                setPagesCount(res.pagesCount)
            })
    }, [searchParams])
    return (
        <>
            <div className='flex flex-col items-center mb-2'>
                <p className='text-slate-700 pt-2'>search question :</p>
                <input type='text' value={searchQuestion} onChange={handleSearch} />
            </div>

            {searchQuestion === '' ? (
                <>
                    {questions.map(q => <QuestionCard key={q.id} question={q} removeQuestion={removeQuestion} />)}
                    <Pagination count={pagesCount} url={`/list/questions`} />
                </>
            ) : (
                <>
                    {allQuestions.map(q => <QuestionCard key={q.id} question={q} removeQuestion={removeQuestion} />)}
                </>
            )}
        </>
    )
}

export default AllQuestions