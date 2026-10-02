import { useTranslation } from 'react-i18next';
import type { Verdict } from '../../lib/types';
import { verdictStyles } from '../../lib/utils';

const RADIUS = 80;
const ARC = Math.PI * RADIUS;

/** Semicircle gauge (0–100). Always drawn left-to-right so the scale reads the same in both languages. */
export function RiskGauge({ score, verdict }: { score: number; verdict: Verdict }) {
  const { t } = useTranslation();
  const filled = (Math.max(0, Math.min(100, score)) / 100) * ARC;

  return (
    <div
      className="relative mx-auto w-48"
      role="meter"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={score}
      aria-label={t('result.score')}
    >
      <svg viewBox="0 0 200 110" className="w-full">
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          strokeWidth="16"
          strokeLinecap="round"
          className="stroke-slate-200 dark:stroke-slate-800"
        />
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={verdictStyles[verdict].stroke}
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={`${filled} ${ARC}`}
          style={{ transition: 'stroke-dasharray 0.8s cubic-bezier(.2,.8,.2,1)' }}
        />
      </svg>
      <div className="absolute inset-x-0 bottom-0 flex flex-col items-center">
        <span className={`text-4xl font-bold tabular-nums ${verdictStyles[verdict].text}`}>
          {score}
        </span>
        <span className="text-xs text-slate-500 dark:text-slate-400">{t('result.outOf')}</span>
      </div>
    </div>
  );
}
