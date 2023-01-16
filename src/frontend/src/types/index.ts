export enum Routes {
  home = '/',
  profile = '/profile',
  singup = '/registry',
  signin = '/login',
  history = '/history',
}

export type THEME = 'light' | 'dark';

export interface LoginData {
  email: string;
  password: string;
}

export type AuthContextType = {
  user: string | null;
  login: (data: LoginData) => Promise<void>;
  logout: () => void;
};
