import { FC, useState} from 'react'
import { Link, useNavigate } from 'react-router-dom';
import { logOut } from '../utils/authUtils';
import useStore from '../zustandStore/store';


interface TLink {
  name: string;
  url: string;
  auth: boolean;
}

const NavLink: FC<TLink> = ({ name, url, auth }) => {
  return (
    <Link to={url} className={`font-bold text-lg h-8 rounded px-2 md:px-7 ${!auth ? 'bg-black text-white-200 ' : 'text-red-200'} md:text-xl hover:cursor-pointer hover:bg-gray-900`}>
      {name}
    </Link>
  )
}

const NavBar: FC = () => {
  const auth = useStore((state) => state.isLoggedIn);
  const setUser = useStore((state) => state.setUser);
  const setIsLoggedIn = useStore((state) => state.setIsLoggedIn);
  const navigate = useNavigate()

  const LogOut = () => {
    logOut()
    setUser(null)
    setIsLoggedIn(false)
    navigate('/signin')
  }

  return (
    <div className='flex justify-between items-center px-3 sm:px-16 h-16 w-full bg-slate-600'>
      <Link to='/' className="text-purple-300 font-extrabold text-2xl md:text-3xl hover:cursor-pointer">
        Quizzio
      </Link>

      <div className={`flex ${auth ? 'justify-between w-[60 %] sm:w-[50%] lg:w-[40%]' : 'justify-end w-[45%]'}`}>
        { auth 
        ? (
          <>
            {[["List", "/categories"], ["Add", "/add"], ["Play", "/play"]].map((el, index) => <NavLink auth key={index} name={el[0]} url={el[1]} />)}
            <button onClick={LogOut} className='bg-red-500 hover:bg-red-600 text-slate-100 p-1 rounded font-extrabold'>Logout</button>
          </>
        )
          : [["Signin", "/signin"], ["Signup", "/signup"]].map((el, index) => <NavLink auth key={index} name={el[0]} url={el[1]} />) }
      </div>
    </div>
  )
}

export default NavBar