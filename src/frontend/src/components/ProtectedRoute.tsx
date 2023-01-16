import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks';
import { ReactElement } from 'react';

const ProtectedRoute = ({ children }: { children: ReactElement }) => {
  const { user } = useAuth();
  return !user ? <Navigate to="/" /> : children;
};

export default ProtectedRoute;
