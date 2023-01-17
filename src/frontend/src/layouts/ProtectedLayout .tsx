import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks';
import { AppBar } from '../components';
import { Button } from '@mui/material';
import { Routes } from '../types';

export default function ProtectedLayout() {
  const { token } = useAuth();
  const { logout } = useAuth();

  const handleClick = () => {
    logout();
  };

  if (!token) {
    return <Navigate to={Routes.home} />;
  }

  return (
    <div>
      <AppBar>
        <Button
          href={Routes.summary}
          color="inherit"
          variant="text"
          sx={{ my: 1, mx: 1.5 }}
        >
          Summary
        </Button>
        <Button
          href={Routes.history}
          color="inherit"
          variant="text"
          sx={{ my: 1, mx: 1.5 }}
        >
          History
        </Button>
        <Button
          href={Routes.profile}
          color="inherit"
          variant="text"
          sx={{ my: 1, mx: 1.5 }}
        >
          Profile
        </Button>
        <Button
          onClick={handleClick}
          variant="outlined"
          sx={{ my: 1, mx: 1.5 }}
        >
          Logout
        </Button>
      </AppBar>
      <Outlet />
    </div>
  );
}
