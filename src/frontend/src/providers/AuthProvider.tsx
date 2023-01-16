import { ReactNode, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocalStorage } from '../hooks';
import { AuthContext } from '../contexts';
import { LoginData, Routes } from '../types';

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
    navigate(Routes.profile);
  };

  const logout = () => {
    setUser(null);
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
