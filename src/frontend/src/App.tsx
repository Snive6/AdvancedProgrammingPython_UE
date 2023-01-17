import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import {
  ErrorPage,
  HistoryPage,
  ProfilePage,
  SignInPage,
  SignUpPage,
  SummaryPage,
} from './pages';
import { ProtectedRoute } from './components';
import { ThemeProvider, createTheme } from '@mui/material';
import React from 'react';
import { AuthLayout, HomeLayout, ProtectedLayout } from './layouts';
import { Routes } from './types';
import { ColorModeContext } from './contexts';

function getUserData(): Promise<string> {
  return new Promise((resolve) => {
    const user = window.localStorage.getItem('user') as string;
    resolve(user);
  });
}

const router = createBrowserRouter([
  {
    element: <AuthLayout />,
    loader: getUserData,
    children: [
      {
        element: <HomeLayout />,
        errorElement: <ErrorPage />,
        children: [
          {
            path: Routes.summary,
            element: <SummaryPage />,
            errorElement: <ErrorPage />,
          },
          {
            path: Routes.home,
            element: <SummaryPage />,
            errorElement: <ErrorPage />,
          },
          {
            path: Routes.singup,
            element: <SignUpPage />,
            errorElement: <ErrorPage />,
          },
          {
            path: Routes.signin,
            element: <SignInPage />,
            errorElement: <ErrorPage />,
          },
        ],
      },
      {
        element: <ProtectedLayout />,
        errorElement: <ErrorPage />,
        children: [
          {
            path: Routes.summary,
            element: <SummaryPage />,
            errorElement: <ErrorPage />,
          },
          {
            path: Routes.history,
            element: <HistoryPage />,
            errorElement: <ErrorPage />,
          },
          {
            path: Routes.profile,
            element: (
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            ),
            errorElement: <ErrorPage />,
          },
        ],
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
        <RouterProvider router={router} />
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
