import { TCategory, TQuestion } from './../utils/fetchDataUtils';
import { mountStoreDevtool } from 'simple-zustand-devtools'
import create from 'zustand'
import {TUser} from '../utils/authUtils'



interface GlobalState {
    user: TUser | null,
    isLoggedIn: boolean,
    categories: TCategory[],
    questions: TQuestion[],
    allQuestions: TQuestion[],
    gameData: {
        score: number;
        quizzQuestions: TQuestion[] | [];
        roundState: 'End' | 'Start';
    },
    setGameScore: (newScore: number) => void,
    setGameQuestions: (newQuestions: TQuestion[]) => void,
    setGameRound: (round: 'End' | 'Start') => void,
    setIsLoggedIn: (authState: boolean) => void
    setUser: (user: TUser | null) => void,
    setCategories: (newCategories: TCategory[]) => void,
    setQuestions: (newQuestions: TQuestion[]) => void,
    setAllQuestions: (newQuestions: TQuestion[]) => void
}


const useStore = create<GlobalState>((set) => ({
    user: null,
    isLoggedIn: false,
    questions: [],
    allQuestions: [],
    categories:[],
    gameData: {
        score: 0,
        quizzQuestions: [],
        roundState: 'End'
    },
    setGameScore: (newScore) => set(state => ({gameData: {...state.gameData, score: newScore}})),
    setGameQuestions: (newQuestions: TQuestion[]) => set(state => ({gameData: {...state.gameData, quizzQuestions: newQuestions}})),
    setGameRound: (round: 'End' | 'Start') => set(state => ({gameData: {...state.gameData, roundState: round}})),
    setIsLoggedIn: (authState) => set({ isLoggedIn: authState }),
    setUser: (user) => set({ user: user }),
    setCategories: (newCategories) => set({ categories: newCategories }),
    setQuestions: (newQuestions) => set({ questions: newQuestions }),
    setAllQuestions: (newQuestions) => set({ allQuestions: newQuestions }),
}))

export default useStore;

if (process.env.NODE_ENV === 'development') {
    mountStoreDevtool('Store', useStore);
}