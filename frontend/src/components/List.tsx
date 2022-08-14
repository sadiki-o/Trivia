import { Outlet, useLocation, useNavigate } from "react-router-dom"

const List = () => {
  const path = useLocation()
  const navigate = useNavigate()

  return (
    <div>
        <div className="mx-auto flex text-white w-[40%] mb-6 mt-3">
            <button onClick={() => navigate('/list/categories')} className={`inline-block rounded-l-[30px] p-3 font-bold w-full h-full text-center ${path.pathname.split('/').includes('categories') ? 'bg-blue-600 text-white' : 'bg-gray-300 text-black'}`}>By Category</button>
            <button onClick={() => navigate('/list/questions')} className={`inline-block rounded-r-[30px] p-3 font-bold w-full h-full text-center ${path.pathname.split('/').includes('questions') ? 'bg-blue-600 text-white' : 'bg-gray-300 text-black'}`}>By Question</button>
        </div>
        <Outlet />
    </div>
  )
}

export default List