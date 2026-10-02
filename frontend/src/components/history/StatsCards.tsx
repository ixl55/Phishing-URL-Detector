import { Activity, ShieldAlert, ShieldCheck, ShieldQuestion } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Stats } from '../../lib/types';
import { cn } from '../../lib/utils';

export function StatsCards({ stats }: { stats: Stats }) {
  const { t } = useTranslation();
  const pct = (n: number) => (stats.total ? Math.round((n / stats.total) * 100) : 0);
  const tiles = [
    {
      label: t('history.total'),
      value: stats.total,
      icon: Activity,
      tone: 'text-brand-600 dark:text-brand-400',
      share: null,
    },
    {
      label: t('verdict.safe'),
      value: stats.safe,
      icon: ShieldCheck,
      tone: 'text-emerald-600 dark:text-emerald-400',
      share: pct(stats.safe),
    },
    {
      label: t('verdict.suspicious'),
      value: stats.suspicious,
      icon: ShieldQuestion,
      tone: 'text-amber-600 dark:text-amber-400',
      share: pct(stats.suspicious),
    },
    {
      label: t('verdict.dangerous'),
      value: stats.dangerous,
      icon: ShieldAlert,
      tone: 'text-red-600 dark:text-red-400',
      share: pct(stats.dangerous),
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {tiles.map(({ label, value, icon: Icon, tone, share }) => (
        <div
          key={label}
          className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
        >
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            {label}
            <Icon className={cn('h-4 w-4', tone)} aria-hidden />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className={cn('text-3xl font-bold tabular-nums', tone)}>{value}</span>
            {share !== null && <span className="text-xs text-slate-400">{share}%</span>}
          </div>
        </div>
      ))}
    </div>
  );
}
