import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../../context/context';


export const PrivateRoute = ({ children }: {children:JSX.Element}) => {
    const appContext = useContext(AuthContext);

    return appContext ? children : <Navigate to="login" replace/>;
};
