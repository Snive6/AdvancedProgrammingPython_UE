import { Container } from '@mui/material';
import { ReactNode } from 'react';

export default function MainContainer({ children }: { children: ReactNode }) {
  return (
    <Container
      component="main"
      maxWidth="md"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      {children}
    </Container>
  );
}
