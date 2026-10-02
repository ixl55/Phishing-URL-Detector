import { useTranslation } from 'react-i18next';
import type { BatchResponse } from '../../lib/types';
import { cn } from '../../lib/utils';

export function BatchSummary({ summary }: { summary: BatchResponse['summary'] }) {
  const { t } = useTranslation();
  const tiles = [
    { label: t('batch.total'), value: summary.total, tone: 'text-slate-900 dark:text-white' },
    {
      label: t('verdict.safe'),
      value: summary.safe,
      tone: 'text-emerald-600 dark:text-emerald-400',
    },
    {
      label: t('verdict.suspicious'),
      value: summary.suspicious,
      tone: 'text-amber-600 dark:text-amber-400',
    },
    {
      label: t('verdict.dangerous'),
      value: summary.dangerous,
      tone: 'text-red-600 dark:text-red-400',
    },
  ];
  if (summary.invalid) {
    tiles.push({ label: t('batch.invalid'), value: summary.invalid, tone: 'text-slate-400' });
  }

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {tiles.map((tile) => (
        <div
          key={tile.label}
          className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
        >
          <div className="text-xs text-slate-500 dark:text-slate-400">{tile.label}</div>
          <div className={cn('mt-1 text-3xl font-bold tabular-nums', tile.tone)}>{tile.value}</div>
        </div>
      ))}
    </div>
  );
}
