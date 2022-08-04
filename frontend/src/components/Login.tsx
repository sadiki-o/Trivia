import React, { FC, useState, useRef } from "react"
import { Link, Navigate } from "react-router-dom"
import { LoginFunc } from "../utils/authUtils"

const Login: FC = () => {
    const errorRef = useRef<HTMLHeadingElement>(null)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const submitLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        const {errorMessage, success} = await LoginFunc({username, password})
        
        if (!success){
            errorRef.current!.innerText! = errorMessage!
        }else{
            <Navigate to='/' replace/>
        }
    }

    return (
        <div className="container w-[80%] sm:w-[50%] max-w-[450px] rounded mx-auto p-4 bg-white mt-10">
            <div className="w-full  mx-auto my-12">
                <h1 className="text-2xl font-medium text-center">Signin</h1>
                <h2 ref={errorRef} className="text-red-500 w-[80%]"></h2>
                <form onSubmit={submitLogin} className="flex flex-col mt-4">
                    <input
                        required
                        onChange={(e) => {
                            setUsername(e.currentTarget.value)
                        }}
                        value={username}
                        type="text"
                        className="px-4 py-3 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
                        placeholder="Username"
                    />
                    <input
                        required
                        onChange={(e) => {
                            setPassword(e.currentTarget.value)
                        }}
                        value={password}
                        type="password"
                        className="px-4 py-3 mt-4 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
                        placeholder="Password"
                    />
                    <button
                        type="submit"
                        className="mt-4 px-4 py-3 text-base rounded-md border border-transparent text-white focus:outline-none bg-blue-500 hover:text-white focus:ring-2 focus:ring-blue-500 cursor-pointer inline-flex items-center w-full justify-center font-lg font-bold"
                    >
                        Login
                    </button>
                    <div className="flex flex-col items-center mt-5">
                        <p className="mt-1 text-medium text-gray-500">
                            New to Here?
                            <Link className="ml-1 font-xl text-blue-700 font-bold" to='/signup'>
                                Sign up now
                            </Link>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Login