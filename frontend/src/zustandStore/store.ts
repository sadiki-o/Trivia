import { mountStoreDevtool } from 'simple-zustand-devtools'
import create from 'zustand'
import {TUser} from '../utils/authUtils'



interface AuthState {
    user: TUser | null,
    isLoggedIn: boolean,
    setIsLoggedIn: (state: boolean) => void
    setUser: (user: TUser | null) => void
}


const useStore = create<AuthState>((set) => ({
    user: null,
    isLoggedIn: false,
    setIsLoggedIn: (state) => set({ isLoggedIn: state }),
    setUser: (user) => set({ user: user })
}))

export default useStore;

if (process.env.NODE_ENV === 'development') {
    mountStoreDevtool('Store', useStore);
}