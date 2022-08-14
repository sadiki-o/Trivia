import axios, { AxiosResponse } from "axios";

const url_path = import.meta.env.VITE_API_URL

export type TUser = {
    id: number
    username: string
}

type TCredentials = {
    username: string;
    password: string;
}

type TResponse = {
    errorMessage: string | null;
    success: boolean;
    user: TUser | null
}


// Authentication functions

export const LoginFunc = async ({ username, password }: TCredentials): Promise<TResponse> => {
    let result: TResponse = {
        errorMessage: null,
        success: false,
        user: null
    }
    await axios.post(
        `${url_path}/signin`,
        {
            username,
            password
        }
    )
        .then((response) => {
            localStorage.setItem('token', response.data['token'])
            result.success = true
            result.user = response.data['user']
        })
        .catch((err) => {
            result.errorMessage = err.response.data;
        })

    return result
}

export const SignupFunc = async ({ username, password }: TCredentials): Promise<TResponse> => {
    let res: TResponse = {
        errorMessage: null,
        success: false,
        user: null
    }

    await axios.post(
        `${url_path}/signup`,
        {
            username,
            password
        }
    )
        .then((response) => {
            res.success = true
        })
        .catch((err) => {
            res.errorMessage = err.response.data.message;
        })

    return res;
}

export const checkAuth = async (): Promise<TUser | null> => {
    let user: TUser | null = null;
    let token: string = localStorage.getItem('token')!

    const config = {
        method: 'post',
        url: `${url_path}/verify`,
        headers: {
            'x-access-token': token
        }
    };

    await axios(config)
        .then((response) => {
            user = response.data['user']
        })
    return user
}

export const logOut = () => {
    localStorage.removeItem('token')
}


