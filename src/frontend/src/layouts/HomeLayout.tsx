import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks';
import { Button } from '@mui/material';
import React from 'react';
import { AppBar } from '../components';
import { Routes } from '../types';

export default function HomeLayout() {
  const { token } = useAuth();

  if (token) {
    return <Navigate to={Routes.summary} />;
  }

  return (
    <React.Fragment>
      <AppBar>
        <Button
          href={Routes.summary}
          color="inherit"
          variant="text"
          sx={{ my: 1, mx: 1.5 }}
        >
          Summary
        </Button>
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
