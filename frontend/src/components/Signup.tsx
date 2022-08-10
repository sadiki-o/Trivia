import { FC, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { SignupFunc } from '../utils/authUtils'

const Signup: FC = () => {
    const errorRef = useRef<HTMLHeadingElement>(null)
    const [username, setUsername] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [confirmPassword, setConfirmPassword] = useState<string>('')

    const submitSignup = async (e: React.FormEvent) => {
        e.preventDefault()
        if(password !== confirmPassword){
            errorRef.current!.innerText! = 'passwords are not identical'
            return
        }else if(password.length < 8){
            errorRef.current!.innerText! = 'password too short'
            return
        }
        const {errorMessage, success} = await SignupFunc({username, password})
        
        if (!success){
            errorRef.current!.innerText! = errorMessage!
        }else{
            errorRef.current!.innerText = ''
            alert('Account created successefully')
            setUsername('')
            setPassword('')
            setConfirmPassword('')
        }
    }

    return (
        <div className="bg-grey-lighter min-h-screen flex flex-col">
            <div className="container max-w-sm mx-auto flex-1 flex flex-col items-center justify-center px-2 pb-40">
                <form onSubmit={submitSignup} className="bg-white px-6 py-8 rounded shadow-md text-black w-full">
                    <h1 className="mb-8 text-3xl text-center">Register</h1>
                    <h2 ref={errorRef} className="text-red-500 w-[80%]"></h2>
                    <input
                        onChange={(e) => {
                            setUsername(e.currentTarget.value)
                        }}
                        value={username}
                        required
                        type="text"
                        className="block border border-grey-light w-full p-3 rounded mb-4"
                        placeholder="Username" />

                    <input
                        onChange={(e) => {
                            setPassword(e.currentTarget.value)
                        }}
                        value={password}
                        required
                        type="password"
                        className="block border border-grey-light w-full p-3 rounded mb-4"
                        placeholder="Password" />
                    <input
                        onChange={(e) => {
                            setConfirmPassword(e.currentTarget.value)
                        }}
                        value={confirmPassword}
                        required
                        type="password"
                        className="block border border-grey-light w-full p-3 rounded mb-4"
                        placeholder="Confirm Password" />

                    <button
                        type='submit'
                        className="w-full text-center py-3 rounded bg-green-400 hover:bg-green-500 text-white hover:bg-green-dark focus:outline-none my-1"
                    >Create Account</button>
                </form>

                <div className="text-gray-500 mt-6">
                    Already have an account? 
                    <Link to='/signin'>
                        <span className="underline-none border-blue font-bold text-blue-700">
                        &nbsp;Log in
                        </span>
                    </Link>
                </div>
            </div>
        </div>
  )
}

export default Signup