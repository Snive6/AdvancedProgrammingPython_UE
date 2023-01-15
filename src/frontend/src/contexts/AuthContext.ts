import { createContext } from 'react';

const AuthContext = createContext<{
  user: string | null;
  login: (data: any) => Promise<void>;
  logout: () => void;
}>({
  user: null,
  login: () => {
    return Promise.resolve();
  },
  logout: () => {},
});

export default AuthContext;
