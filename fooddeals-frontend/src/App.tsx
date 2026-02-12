import { Routes, Route } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { FoodVisionPage } from './pages/FoodVisionPage';
import { ResetPasswordPage } from './pages/ResetPasswordPage';
import { SettingsPage } from './pages/SettingsPage';
import { VideoChatPage } from './pages/VideoChatPage';

function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/food-vision" element={<FoodVisionPage />} />
        <Route path="/video-chat" element={<VideoChatPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/auth/login" element={<LoginPage />} />
        <Route path="/auth/register" element={<RegisterPage />} />
        <Route path="/auth/forgot" element={<ForgotPasswordPage />} />
        <Route path="/auth/reset" element={<ResetPasswordPage />} />
      </Routes>
    </AppShell>
  );
}

export default App;
