interface HealthGaugeProps {
  score: number;
}

export default function HealthGauge({ score }: HealthGaugeProps) {
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : score >= 40 ? '#ef4444' : '#7f1d1d';

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 120 120" className="w-28 h-28 -rotate-90">
        <circle cx="60" cy="60" r={radius} stroke="#374151" strokeWidth="10" fill="none" />
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="mt-2 text-center">
        <p className="text-2xl font-semibold text-white">{score.toFixed(0)}%</p>
        <p className="text-xs text-gray-400">Health score</p>
      </div>
    </div>
  );
}
