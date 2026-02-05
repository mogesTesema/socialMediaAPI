import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';

const rootElement = document.getElementById('root');

async function startApp() {
  if (!rootElement) {
    return;
  }

  try {
    const [{ default: App }, { AuthProvider }, { ErrorBoundary }] = await Promise.all([
      import('./App.tsx'),
      import('./features/auth/AuthContext'),
      import('./components/ErrorBoundary'),
    ]);

    createRoot(rootElement).render(
      <StrictMode>
        <ErrorBoundary>
          <AuthProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </AuthProvider>
        </ErrorBoundary>
      </StrictMode>,
    );

    (window as unknown as { __APP_MOUNTED__?: boolean }).__APP_MOUNTED__ = true;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    rootElement.innerHTML = `Failed to load UI: ${message}`;
    console.error('Failed to start app', error);
  }
}

void startApp();
