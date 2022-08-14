import { FC, MouseEvent } from "react"
import { useNavigate, useSearchParams } from 'react-router-dom';

const Pagination = ({ count, url }: { count: number, url: string }) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate()

  const Navigate = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    navigate(`${url}?page=${e.currentTarget.id}`)    
  }

  return count > 1 ? (
  <div className="flex container justify-center gap-1 mx-auto">
    {new Array(count).fill(0).map((el, index) => <button id={(index + 1).toString()} key={index + 1} onClick={Navigate} className={`rounded-full border-black border-2 px-2 ${parseInt(searchParams.get('page')!) === index + 1 || (!parseInt(searchParams.get('page')!) && index === 0) ? 'text-white bg-black' : 'text-black'}`}>{index+1}</button>)}
  </div>
  ) : (
    <></>
  )

}

export default Pagination