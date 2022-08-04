import axios from "axios";

const url_path = import.meta.env.VITE_API_URL

type TCredentials = {
    username: string;
    password: string;
}

type TResponse = {
    errorMessage: string | null ;
    success: boolean ;
}


export const LoginFunc = async ({username, password}: TCredentials): Promise<TResponse> => {
    let result: TResponse = {
        errorMessage: null,
        success: false
    }
    await axios.post(
        `${url_path}/login`,
        {
            username,
            password
        }
    )
    .then((response) => {
        localStorage.setItem('token', response.data['token'])
        result.success = true
    })
    .catch((err) => {
        result.errorMessage = err.response.data;
    })
    window.location.href = '/'
    return result
}

export const SignupFunc = async ({username, password}: TCredentials): Promise<TResponse>  => {
    let res: TResponse = {
        errorMessage: null,
        success: false
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

export const checkAuth = async (): Promise<boolean> => {
    let token: string = localStorage.getItem('token')!
    var config = {
        method: 'post',
        url: `${url_path}/verify`,
        headers: {
            'x-access-token': token
        }
    };
    let success: boolean = false;
    await axios(config)
    .then((response) => {
        success = true
    })
    
    return success
}

export const logOut = () => {
    localStorage.removeItem('token')
    window.location.href = '/login'
}