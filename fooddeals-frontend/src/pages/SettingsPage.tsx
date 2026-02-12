import { useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { SectionHeader } from '../components/SectionHeader';
import { useAuth } from '../features/auth/AuthContext';
import { api } from '../lib/api';
import { useNavigate } from 'react-router-dom';

export function SettingsPage() {
  const { accessToken, user, clearSession } = useAuth();
  const [status, setStatus] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogout = () => {
    clearSession();
    navigate('/');
  };

  const handleDeleteAccount = async () => {
     if (!accessToken) return;
     if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) return;
     
     try {
       await api.deleteAccount(accessToken);
       clearSession();
       navigate('/');
     } catch (error) {
       setStatus(error instanceof Error ? error.message : 'Failed to delete account');
     }
  };

  if (!user) {
    return (
       <div className="text-center py-12 text-slate-400">
          Please sign in to manage your settings.
       </div>
    );
  }

  return (
    <div className="space-y-8 max-w-2xl mx-auto">
      <SectionHeader 
         title="Account Settings" 
         subtitle="Manage your profile and security preferences."
      />
      
      <Card className="space-y-6 border-slate-700 bg-slate-800/30">
         <div className="space-y-1 border-b border-slate-700 pb-4">
            <h3 className="text-lg font-medium text-white">Profile</h3>
            <div className="grid grid-cols-[100px_1fr] gap-4 items-center text-sm py-2">
               <span className="text-slate-400">Email</span>
               <span className="text-slate-200">{user.email}</span>
            </div>
             <div className="grid grid-cols-[100px_1fr] gap-4 items-center text-sm py-2">
               <span className="text-slate-400">Status</span>
               <span className="text-slate-200">
                  {user.confirmed ? (
                     <span className="text-emerald-400">Verified</span>
                  ) : (
                     <span className="text-amber-400">Unverified</span>
                  )}
               </span>
            </div>
         </div>

         <div className="pt-2">
            <h3 className="text-lg font-medium text-white mb-4">Danger Zone</h3>
            <div className="flex flex-col gap-4">
               <div className="p-4 rounded-xl border border-rose-500/20 bg-rose-500/5 flex items-center justify-between">
                  <div>
                     <div className="text-rose-200 font-medium">Sign Out</div>
                     <div className="text-rose-200/60 text-xs">End your current session.</div>
                  </div>
                  <Button tone="secondary" onClick={handleLogout} className="border-rose-500/30 text-rose-200 hover:bg-rose-500/10">
                     Sign Out
                  </Button>
               </div>

               <div className="p-4 rounded-xl border border-red-500/20 bg-red-500/5 flex items-center justify-between">
                  <div>
                     <div className="text-red-200 font-medium">Delete Account</div>
                     <div className="text-red-200/60 text-xs">Permanently remove your account and data.</div>
                  </div>
                  <Button tone="secondary" onClick={handleDeleteAccount} className="bg-red-500/10 border-red-500/30 text-red-200 hover:bg-red-500/20">
                     Delete Account
                  </Button>
               </div>
            </div>
         </div>

         {status && (
            <div className="text-sm text-rose-300 text-center">
               {status}
            </div>
         )}
      </Card>
    </div>
  );
}
