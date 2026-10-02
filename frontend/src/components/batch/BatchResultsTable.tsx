import { Fragment, useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { BatchItem, Lang } from '../../lib/types';
import { cn, verdictStyles } from '../../lib/utils';
import { FindingsList } from '../scan/FindingsList';
import { VerdictBadge } from '../scan/VerdictBadge';

export function BatchResultsTable({ items }: { items: BatchItem[] }) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language as Lang;
  const [open, setOpen] = useState<number | null>(null);

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <table className="w-full table-fixed text-sm">
        <thead className="bg-slate-50 text-xs text-slate-500 dark:bg-slate-800/50 dark:text-slate-400">
          <tr>
            <th className="px-4 py-3 text-start font-medium">{t('batch.link')}</th>
            <th className="w-20 px-4 py-3 text-start font-medium">{t('batch.score')}</th>
            <th className="w-28 px-4 py-3 text-start font-medium">{t('batch.verdict')}</th>
            <th className="w-24 px-4 py-3 text-end font-medium">{t('batch.details')}</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
          {items.map((item, index) => {
            const result = item.result;
            const expanded = open === index;
            return (
              <Fragment key={index}>
                <tr className="align-middle">
                  <td className="max-w-0 px-4 py-3">
                    <span
                      dir="ltr"
                      className="block truncate font-mono text-xs text-slate-700 dark:text-slate-300"
                      title={item.input}
                    >
                      {item.input}
                    </span>
                  </td>
                  <td
                    className={cn(
                      'px-4 py-3 font-semibold tabular-nums',
                      result && verdictStyles[result.verdict].text,
                    )}
                  >
                    {result ? result.score : '—'}
                  </td>
                  <td className="px-4 py-3">
                    {result ? (
                      <VerdictBadge verdict={result.verdict} size="sm" />
                    ) : (
                      <span className="text-xs text-slate-400">{item.error?.[lang]}</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-end">
                    {result && (
                      <button
                        type="button"
                        onClick={() => setOpen(expanded ? null : index)}
                        className="inline-flex items-center gap-1 rounded-lg px-2 py-1 text-xs text-brand-600 hover:bg-brand-50 dark:text-brand-400 dark:hover:bg-brand-950"
                        aria-expanded={expanded}
                      >
                        {expanded ? t('batch.hide') : t('batch.show')}
                        <ChevronDown
                          className={cn(
                            'h-3.5 w-3.5 transition-transform',
                            expanded && 'rotate-180',
                          )}
                        />
                      </button>
                    )}
                  </td>
                </tr>
                {expanded && result && (
                  <tr>
                    <td colSpan={4} className="bg-slate-50/60 px-4 py-4 dark:bg-slate-950/40">
                      <p
                        className={cn(
                          'mb-3 text-sm font-medium',
                          verdictStyles[result.verdict].text,
                        )}
                      >
                        {result.advice[lang]}
                      </p>
                      <FindingsList findings={result.findings} />
                    </td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
