import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { checkAuth } from '../../utils/authUtils';
import Login from '../Login';
import {useState} from 'react';
import useStore from '../../zustandStore/store';


export const PrivateRoute = () => {
    const auth = useStore((state) => state.isLoggedIn);

    return auth ? <Outlet /> : <Login />;
};
