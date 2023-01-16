import { createContext } from 'react';
import { AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType>({
  user: null,
  login: () => {
    return Promise.resolve();
  },
  logout: () => {},
});

export default AuthContext;
