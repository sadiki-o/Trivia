import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import NavBar from './components/NavBar'
import './index.css'
import { AuthContext } from './context/context';
import { checkAuth } from './utils/authUtils'

const Main = () => {
  const [auth, setAuth] = useState(false)

  useEffect(() => {
    (async () => {
      const res = await checkAuth()      
      setAuth(res)
    })()
  }, [auth])

  return (
    <AuthContext.Provider value={auth}>
      <React.StrictMode>
        <BrowserRouter>
          <NavBar />
          <App />
        </BrowserRouter>
      </React.StrictMode>
    </AuthContext.Provider>
  )
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(<Main/>)
