import axios from 'axios';

export type TCategory = {
    id?: number;
    type: string;
    ownership?: number
}

export type TQuestion = {
    id?: number
    question: string
    answer: string
    category: number
    difficulty: number,
    avg_rating?: number,
    ownership?: number,
    rating?: number
}


const url_path = import.meta.env.VITE_API_URL

// App functions
export const getCategories = async (): Promise<TCategory[]> => {
    let token: string = localStorage.getItem('token')!

    let categories: TCategory[] = [];

    var config = {
        method: 'get',
        url: `${url_path}/categories`,
        headers: {
            'x-access-token': token
        }
    };
    await axios(config)
        .then((response) => {
            categories = response.data['categories']
        }) 
    return categories;
}

export const getQuestions = async (category: number, page: number): Promise<{
    questions: TQuestion[],
    pagesCount: number
}> => {
    let token: string = localStorage.getItem('token')!

    let questions: TQuestion[] = [];
    let pagesCount: number = 0;

    var config = {
        method: 'get',
        url: `${url_path}/category/${category}?page=${page ? page : 1}`,
        headers: {
            'x-access-token': token
        }
    };
    await axios(config)
        .then((response) => {
            questions = response.data['questions']
            pagesCount = response.data['pages']
        })

    return {
        questions,
        pagesCount
    }
}

export const addQuestion = async (question: TQuestion): Promise<boolean> => {
    let token: string = localStorage.getItem('token')!
    let res: boolean = false;

    var config = {
        method: 'post',
        url: `${url_path}/questions`,
        headers: {
            'x-access-token': token,
        },
        data: {
            question: question.question,
            answer: question.answer,
            difficulty: question.difficulty,
            category_id: question.category,
        }
    };
    await axios(config)
        .then((response) => {
            res = true
        })

    return res
}

export const addCategory = async (category: string): Promise<boolean> => {
    let token: string = localStorage.getItem('token')!
    let res: boolean = false;

    var config = {
        method: 'post',
        url: `${url_path}/categories`,
        headers: {
            'x-access-token': token,
        },
        data: {
            category
        }
    };
    await axios(config)
        .then((response) => {
            res = true
        })

    return res
}

export const deleteQuestion = async (question_id: number): Promise<boolean> => {
    let token: string = localStorage.getItem('token')!
    let res: boolean = false;

    var config = {
        method: 'delete',
        url: `${url_path}/questions`,
        headers: {
            'x-access-token': token,
        },
        data: {
            question_id
        }
    };
    await axios(config)
        .then((response) => {
            res = true
        })

    return res
}

export const addOrUpdateRating = async (question_id: number, rating: number): Promise<{res:boolean, medium: number}> => {
    let token: string = localStorage.getItem('token')!
    let res: boolean = false;
    let medium: number = 0;

    var config = {
        method: 'post',
        url: `${url_path}/ratings`,
        headers: {
            'x-access-token': token,
        },
        data: {
            question_id,
            rating
        }
    };
    await axios(config)
        .then((response) => {
            res = true
            medium = response.data['medium']
        })

    return { res, medium }
}

export const deleteCategory = async (category_id: number): Promise<boolean> => {
    let token: string = localStorage.getItem('token')!
    let res: boolean = false;

    var config = {
        method: 'delete',
        url: `${url_path}/categories`,
        headers: {
            'x-access-token': token,
        },
        data: {
            category_id
        }
    };
    await axios(config)
        .then((response) => {
            res = true
        })

    return res
}