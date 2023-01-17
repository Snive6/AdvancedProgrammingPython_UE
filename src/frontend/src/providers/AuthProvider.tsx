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
  const [user, setUser] = useLocalStorage('user', userData);
  const navigate = useNavigate();

  const login = async (data: LoginData) => {
    setUser(data.email);
    axios.post(`${ApiUrlAdres}/login`);
    navigate(Routes.profile);
  };

  const logout = () => {
    setUser(null);
    axios.post(`${ApiUrlAdres}/logout`);
    navigate(Routes.home, { replace: true });
  };

  const value = useMemo(
    () => ({
      user,
      login,
      logout,
    }),
    [user],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
