import { createContext } from 'react';
import { AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType>({
  token: null,
  login: () => {
    return Promise.resolve();
  },
  logout: () => {},
});

export default AuthContext;
