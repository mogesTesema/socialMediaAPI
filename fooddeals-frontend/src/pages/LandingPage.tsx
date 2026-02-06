import { Link } from 'react-router-dom';
import { Badge } from '../components/Badge';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { AnimatedBackground } from '../components/AnimatedBackground';

export function LandingPage() {
  return (
    <div className="relative overflow-hidden">
      <AnimatedBackground />
      <div className="absolute inset-0 bg-sky-900/30 backdrop-blur-sm" />
      <div className="relative z-10 space-y-12">
        <section className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-6">
            <Badge>Production Ready</Badge>
            <h1 className="text-4xl font-semibold leading-tight text-white lg:text-5xl">
              FoodDeals enterprise console for food posts, engagement, and intelligence.
            </h1>
            <p className="text-lg text-amber-100/80">
              Manage posts, moderate comments, track likes, and run ML food vision
              predictions in a unified platform. Built for fast iteration and enterprise
              scale.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link to="/dashboard">
                <Button>Open dashboard</Button>
              </Link>
              <Link to="/food-vision">
                <Button tone="secondary">Food vision lab</Button>
              </Link>
            </div>
          </div>
          <Card className="space-y-4">
            <h2 className="text-xl font-semibold text-white">What’s inside</h2>
            <ul className="space-y-3 text-sm text-amber-100/80">
              <li>• Auth, sessions, and recovery workflows</li>
              <li>• Content operations with likes + comments</li>
              <li>• ML-powered food classification</li>
              <li>• Ready for recommendations + ordering</li>
            </ul>
          </Card>
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            {
              label: 'Role-based dashboards & workflows',
              classes: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100',
            },
            {
              label: 'Typed API contracts',
              classes: 'border-sky-500/30 bg-sky-500/10 text-sky-100',
            },
            {
              label: 'Docker-first development',
              classes: 'border-violet-500/30 bg-violet-500/10 text-violet-100',
            },
          ].map((item) => (
            <div
              key={item.label}
              className={`rounded-2xl border p-4 text-sm ${item.classes}`}
            >
              {item.label}
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
