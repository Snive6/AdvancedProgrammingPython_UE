import { ReactNode, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocalStorage } from '../hooks';
import { AuthContext } from '../contexts';
import { ApiUrlAdres, LoginData, Routes } from '../types';
import axios from 'axios';

export default function AuthProvider({
  children,
  userData = null,
}: {
  children: ReactNode;
  userData?: string | null;
}) {
  const [token, setToken] = useLocalStorage('token', userData);
  const navigate = useNavigate();

  const login = async (data: LoginData) => {
    setToken(data.email);
    axios.post(`${ApiUrlAdres}/login`);
    navigate(Routes.profile);
  };

  const logout = () => {
    setToken(null);
    axios.post(`${ApiUrlAdres}/logout`);
    navigate(Routes.home, { replace: true });
  };

  const value = useMemo(
    () => ({
      token,
      login,
      logout,
    }),
    [token],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
