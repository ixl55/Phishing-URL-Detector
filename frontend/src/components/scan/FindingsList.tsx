import { AlertTriangle, CircleCheck, Info, OctagonAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Finding, Lang } from '../../lib/types';
import { cn, severityStyles } from '../../lib/utils';

const icons = { high: OctagonAlert, medium: AlertTriangle, low: Info };
const iconColors = {
  high: 'text-red-600 dark:text-red-400',
  medium: 'text-amber-600 dark:text-amber-400',
  low: 'text-sky-600 dark:text-sky-400',
};

export function FindingsList({ findings }: { findings: Finding[] }) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language as Lang;

  if (findings.length === 0) {
    return (
      <p className="flex items-center gap-2 text-sm text-emerald-700 dark:text-emerald-300">
        <CircleCheck className="h-4 w-4" aria-hidden />
        {t('result.noReasons')}
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {findings.map((f) => {
        const Icon = icons[f.severity];
        return (
          <li
            key={f.rule_id}
            className="flex gap-3 rounded-xl border border-slate-100 bg-slate-50/60 p-3 dark:border-slate-800 dark:bg-slate-800/40"
          >
            <Icon className={cn('mt-0.5 h-5 w-5 shrink-0', iconColors[f.severity])} aria-hidden />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium text-slate-900 dark:text-slate-100">
                  {f.title[lang]}
                </span>
                <span
                  className={cn(
                    'rounded-full px-2 py-0.5 text-[11px] font-semibold',
                    severityStyles[f.severity],
                  )}
                >
                  {t(`severity.${f.severity}`)} · +{f.weight}
                </span>
              </div>
              <p className="mt-1 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
                {f.detail[lang]}
              </p>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
