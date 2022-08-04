import { FC } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import AddQuestion from "./components/AddQuestion"
import Home from "./components/Home"
import Login from "./components/Login"
import Play from "./components/Play"
import Signup from "./components/Signup"
import './App.css'
import { PrivateRoute } from "./components/Restrict/PrivateRoute"
import Add from "./components/Add"
import { PublicRoute } from "./components/Restrict/PublicRoute"


const App: FC = () => {

  return (
    <Routes>
      <Route path='/'>
        <Route index element={
          <PrivateRoute>
            <Home />
          </PrivateRoute>
        } />
        <Route path="add" element={
          <PrivateRoute>
            <Add />
          </PrivateRoute>
        }></Route>
        <Route path="play" element={
          <PrivateRoute>
            <Play />
          </PrivateRoute>
        }> </Route>
        <Route path="add" element={
          <PrivateRoute>
            <AddQuestion />
          </PrivateRoute>
        }> </Route>
        
        <Route path='signin' element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        } />
        <Route path="signup" element={
          <PublicRoute>
            <Signup />
          </PublicRoute>
        } />
      </Route>
      <Route
        path="*"
        element={<Navigate to='login' replace />}
      />
    </Routes>
  )
}

export default App
