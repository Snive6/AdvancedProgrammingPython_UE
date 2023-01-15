import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import {
  ErrorPage,
  ProfilePage,
  RootPage,
  SignInPage,
  SignOutPage,
  SignUpPage,
} from './pages';
import { ProtectedRoute } from './components';
import { ThemeProvider, createTheme } from '@mui/material';
import React from 'react';
import { ColorModeContext } from './contexts';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootPage />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: '/register',
        element: <SignUpPage />,
        errorElement: <ErrorPage />,
      },
      {
        path: '/login',
        element: <SignInPage />,
        errorElement: <ErrorPage />,
      },
      {
        path: '/logout',
        element: <SignOutPage />,
        errorElement: <ErrorPage />,
      },
      {
        path: '/profile',
        element: (
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        ),
        errorElement: <ErrorPage />,
      },
    ],
  },
]);

function App() {
  const [mode, setMode] = React.useState<'light' | 'dark'>('light');
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
        },
      }),
    [mode],
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />;
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
