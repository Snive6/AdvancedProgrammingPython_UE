import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks';
import { Button } from '@mui/material';
import React from 'react';
import { AppBar } from '../components';
import { Routes } from '../types';

export default function HomeLayout() {
  const { user } = useAuth();

  if (user) {
    return <Navigate to={Routes.history} />;
  }

  return (
    <React.Fragment>
      <AppBar>
        <Button href={Routes.signin} variant="outlined" sx={{ my: 1, mx: 1.5 }}>
          Login
        </Button>
        <Button href={Routes.singup} variant="outlined" sx={{ my: 1, mx: 1.5 }}>
          Registry
        </Button>
      </AppBar>
      <Outlet />
    </React.Fragment>
  );
}
