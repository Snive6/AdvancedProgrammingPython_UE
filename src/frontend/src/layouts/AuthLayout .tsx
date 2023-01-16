import { Suspense } from 'react';
import { useLoaderData, Await, Outlet } from 'react-router-dom';
import LinearProgress from '@mui/material/LinearProgress';
import Alert from '@mui/material/Alert';
import { AuthProvider } from '../providers';

export default function AuthLayout() {
  const userPromise = useLoaderData() as Promise<string>;

  return (
    <Suspense fallback={<LinearProgress />}>
      <Await
        resolve={userPromise}
        errorElement={<Alert severity="error">Something went wrong!</Alert>}
        children={(user) => (
          <AuthProvider userData={user}>
            <Outlet />
          </AuthProvider>
        )}
      />
    </Suspense>
  );
}
