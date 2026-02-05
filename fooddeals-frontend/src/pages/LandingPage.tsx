import { Badge } from '../components/Badge';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Link } from 'react-router-dom';

export function LandingPage() {
  return (
    <div className="space-y-12">
      <section className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <Badge>Production Ready</Badge>
          <h1 className="text-4xl font-semibold leading-tight text-white lg:text-5xl">
            FoodDeals enterprise console for food posts, engagement, and intelligence.
          </h1>
          <p className="text-lg text-slate-300">
            Manage posts, moderate comments, track likes, and run ML food vision predictions
            in a unified platform. Built for fast iteration and enterprise scale.
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
          <ul className="space-y-3 text-sm text-slate-300">
            <li>• Auth, sessions, and recovery workflows</li>
            <li>• Content operations with likes + comments</li>
            <li>• ML-powered food classification</li>
            <li>• Ready for recommendations + ordering</li>
          </ul>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          'Role-based dashboards & workflows',
          'Typed API contracts',
          'Docker-first development',
        ].map((item) => (
          <div
            key={item}
            className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4 text-sm text-slate-200"
          >
            {item}
          </div>
        ))}
      </section>
    </div>
  );
}
