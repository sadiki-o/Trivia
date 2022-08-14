import { FC, useEffect, useState } from 'react';
import { Route, Routes } from "react-router-dom"
import Home, { QuestionsDisplay } from "./components/Home"
import Login from "./components/Login"
import Play from "./components/Play"
import Signup from "./components/Signup"
import './App.css'
import { PrivateRoute } from "./components/Restrict/PrivateRoute"
import { PublicRoute } from "./components/Restrict/PublicRoute"
import { checkAuth } from './utils/authUtils';
import useStore from './zustandStore/store';
import Spinner from './components/Spinner';
import NavBar from './components/NavBar';
import Add from './components/Add';
import Main from './components/Main';
import List from './components/List';
import AllQuestions from './components/AllQuestions';


const App: FC = () => {
  const setUser = useStore(state => state.setUser)
  const setIsLoggedIn = useStore(state => state.setIsLoggedIn)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    (async () => {
      const user = await checkAuth()
      if (user) {
        setIsLoggedIn(true)
        setUser(user)
      } else {
        setIsLoggedIn(false)
        setUser(null)
      }
    })()

  }, [])


  useEffect(() => {
    const timeOutId = setTimeout(() => {
      setLoading(false)
    }, 1000)

    return () => clearTimeout(timeOutId)

  }, [])


  return loading ? <Spinner /> : (
    <div>
      <NavBar />
      <Routes>
        <Route path='/' element={<Main />}/>
        <Route element={<PrivateRoute />}>
          <Route path='list' element={<List />}>
            <Route path='categories' element={<Home />}>
              <Route path=':categoryid' element={<QuestionsDisplay />}/>
            </Route>
            <Route path='questions' element={<AllQuestions />}/>
          </Route>
          <Route path="add" element={<Add />} />
          <Route path="play" element={<Play />} >
          </Route>
        </Route>

        <Route element={<PublicRoute />}>
          <Route path='signin' element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>
          
      </Routes>
    </div>

  )
}

export default App
