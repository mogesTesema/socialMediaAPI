const assets = [
  '/backgrounds/hamburger_1.webp',
  '/backgrounds/hambergur_2.webp',
  '/backgrounds/ice_cream.jpg',
  '/backgrounds/ice_cream_1.webp',
  '/backgrounds/steak.png',
  '/backgrounds/steak2.png',
  '/backgrounds/steak3.png',
  '/backgrounds/sushi.webp',
];

const placements = [
  { top: '6%', left: '6%', size: '160px', delay: '0s' },
  { top: '12%', right: '8%', size: '140px', delay: '1s' },
  { top: '48%', left: '4%', size: '180px', delay: '2s' },
  { top: '62%', right: '6%', size: '160px', delay: '1.5s' },
  { bottom: '8%', left: '18%', size: '140px', delay: '0.5s' },
  { bottom: '6%', right: '16%', size: '180px', delay: '2.5s' },
  { top: '30%', left: '38%', size: '120px', delay: '3s' },
  { top: '24%', right: '38%', size: '120px', delay: '3.5s' },
];

export function AnimatedBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-950 to-slate-900" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.15),_transparent_55%)]" />
      {assets.map((src, index) => (
        <div
          key={src}
          className="bg-float absolute opacity-30 blur-[0.2px]"
          style={{
            ...placements[index],
            width: placements[index].size,
            height: placements[index].size,
            animationDelay: placements[index].delay,
          }}
        >
          <img
            src={src}
            alt=""
            className="h-full w-full rounded-3xl object-cover shadow-2xl"
          />
        </div>
      ))}
    </div>
  );
}
