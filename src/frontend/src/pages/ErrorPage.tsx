import { useRouteError } from 'react-router-dom';
import { MainContainer } from '../components';

export default function ErrorPage() {
  const error: { statusText: any; message: any } = useRouteError() as {
    statusText: any;
    message: any;
  };
  console.error(error);

  return (
    <MainContainer>
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>{error.statusText || error.message}</i>
      </p>
    </MainContainer>
  );
}
