import { Outlet } from 'react-router-dom';
import Home from '../Home';
import { checkAuth } from '../../utils/authUtils';
import { useEffect, useState } from 'react';
import useStore from '../../zustandStore/store';


export const PublicRoute = () => {
    const auth = useStore((state) => state.isLoggedIn);

    return !auth ? <Outlet /> : <Home />;
};
