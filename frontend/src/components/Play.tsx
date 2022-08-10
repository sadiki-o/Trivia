import {FC, useEffect, useState} from 'react'
import { getCategories, TCategory } from '../utils/fetchDataUtils'

const Play: FC = () => {
  const [categories, setCategories] = useState<TCategory[]>([])

  useEffect(() => {
    getCategories()
      .then(res => {
        setCategories(res)
      }).catch(err => {
        console.log(err);
      })
  }, [])
  return (
    <div className='flex flex-col items-center pt-10'>
      <li>All categories</li>
      {categories.map((el) => <li key={el.id}>{el.type}</li>)}
    </div>
  )
}

export default Play