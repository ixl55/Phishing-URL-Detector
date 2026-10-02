import { Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Scan } from '../../lib/types';
import { cn, formatDate, verdictStyles } from '../../lib/utils';
import { VerdictBadge } from '../scan/VerdictBadge';

interface Props {
  scans: Scan[];
  onDelete: (id: number) => void;
}

export function HistoryTable({ scans, onDelete }: Props) {
  const { t, i18n } = useTranslation();

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[640px] text-sm">
        <thead className="text-xs text-slate-500 dark:text-slate-400">
          <tr className="border-b border-slate-200 dark:border-slate-800">
            <th className="px-3 py-2 text-start font-medium">{t('batch.link')}</th>
            <th className="px-3 py-2 text-start font-medium">{t('batch.score')}</th>
            <th className="px-3 py-2 text-start font-medium">{t('batch.verdict')}</th>
            <th className="px-3 py-2 text-start font-medium">{t('history.source')}</th>
            <th className="px-3 py-2 text-start font-medium">{t('history.date')}</th>
            <th className="px-3 py-2" />
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
          {scans.map((scan) => (
            <tr key={scan.id}>
              <td className="max-w-[280px] px-3 py-2.5">
                <span
                  dir="ltr"
                  className="block truncate font-mono text-xs text-slate-700 dark:text-slate-300"
                  title={scan.url}
                >
                  {scan.url}
                </span>
              </td>
              <td
                className={cn(
                  'px-3 py-2.5 font-semibold tabular-nums',
                  verdictStyles[scan.verdict].text,
                )}
              >
                {scan.score}
              </td>
              <td className="px-3 py-2.5">
                <VerdictBadge verdict={scan.verdict} size="sm" />
              </td>
              <td className="px-3 py-2.5 text-xs text-slate-500">
                {t(`history.sources.${scan.source}`)}
              </td>
              <td className="whitespace-nowrap px-3 py-2.5 text-xs text-slate-500">
                {formatDate(scan.created_at, i18n.language)}
              </td>
              <td className="px-3 py-2.5 text-end">
                <button
                  type="button"
                  onClick={() => onDelete(scan.id)}
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950"
                  aria-label={t('history.delete')}
                  title={t('history.delete')}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
