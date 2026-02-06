import { Component, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  message?: string;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, message: error.message };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '24px', color: '#f8fafc', background: '#0b2a4a' }}>
          <h1 style={{ fontSize: '20px', marginBottom: '8px' }}>UI failed to load</h1>
          <p style={{ fontSize: '14px', color: '#cbd5f5' }}>{this.state.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
