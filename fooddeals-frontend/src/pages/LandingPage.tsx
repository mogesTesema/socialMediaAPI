import { Link } from 'react-router-dom';
import { Badge } from '../components/Badge';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { AnimatedBackground } from '../components/AnimatedBackground';

export function LandingPage() {
  return (
    <div className="relative overflow-hidden">
      <AnimatedBackground />
      <div className="absolute inset-0 bg-gradient-to-b from-primary-950/20 to-transparent backdrop-blur-sm" />
      <div className="relative z-10 space-y-16">
        <section className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] pt-8">
          <div className="space-y-8">
            <Badge>🚀 Production Ready</Badge>
            <div>
              <h1 className="text-5xl sm:text-6xl font-black leading-tight bg-gradient-to-r from-primary-300 via-accent-emerald to-accent-cyan bg-clip-text text-transparent lg:text-7xl">
                FoodDeals Community Hub
              </h1>
              <p className="text-xl text-slate-300 mt-4 leading-relaxed">
                Share food deals, engage with posts, build communities. A modern platform for food enthusiasts built with React and FastAPI for scale, speed, and reliability.
              </p>
            </div>
            <div className="flex flex-wrap gap-4 pt-4">
              <Link to="/dashboard">
                <Button className="px-8 py-3 font-bold text-lg">Explore Dashboard</Button>
              </Link>
              <Link to="/food-vision">
                <Button tone="secondary" className="px-8 py-3 font-bold text-lg">Try Food Vision</Button>
              </Link>
            </div>
          </div>
          <Card variant="cyan" className="space-y-5">
            <h2 className="text-2xl font-bold text-accent-cyan/90">✨ Key Features</h2>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-accent-emerald mt-1">✓</span>
                <span>User authentication & secure sessions</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-accent-emerald mt-1">✓</span>
                <span>Posts with rich engagement (likes & comments)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-accent-emerald mt-1">✓</span>
                <span>AI-powered food classification</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-accent-emerald mt-1">✓</span>
                <span>Real-time video chat integration</span>
              </li>
            </ul>
          </Card>
        </section>

        <section className="grid gap-4 md:grid-cols-3 py-8">
          {[
            {
              icon: '🎨',
              label: 'Modern UI Design',
              desc: 'Beautiful, responsive interface with smooth animations',
              variant: 'emerald' as const,
            },
            {
              icon: '⚡',
              label: 'High Performance',
              desc: 'Built for speed with optimized React & FastAPI backend',
              variant: 'primary' as const,
            },
            {
              icon: '🔒',
              label: 'Secure & Scalable',
              desc: 'Enterprise-grade security with Docker containerization',
              variant: 'purple' as const,
            },
          ].map((item) => (
            <Card key={item.label} variant={item.variant} className="space-y-3">
              <div className="text-4xl">{item.icon}</div>
              <h3 className="font-bold text-lg text-slate-100">{item.label}</h3>
              <p className="text-sm text-slate-300">{item.desc}</p>
            </Card>
          ))}
        </section>
      </div>
    </div>
  );
}
