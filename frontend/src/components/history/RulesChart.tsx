import { useTranslation } from 'react-i18next';
import type { Lang, Stats } from '../../lib/types';

/** Horizontal bars of the most frequent rules; bars grow from the reading-start edge. */
export function RulesChart({ rules }: { rules: Stats['top_rules'] }) {
  const { i18n } = useTranslation();
  const lang = i18n.language as Lang;
  const max = Math.max(1, ...rules.map((r) => r.count));

  return (
    <ul className="space-y-3">
      {rules.map((rule) => (
        <li key={rule.rule_id}>
          <div className="mb-1 flex items-baseline justify-between gap-2 text-sm">
            <span className="truncate text-slate-700 dark:text-slate-300">{rule.title[lang]}</span>
            <span className="font-semibold tabular-nums text-slate-900 dark:text-white">
              {rule.count}
            </span>
          </div>
          <div className="h-2 rounded-full bg-slate-100 dark:bg-slate-800">
            <div
              className="h-2 rounded-full bg-brand-500 transition-all"
              style={{ width: `${(rule.count / max) * 100}%` }}
            />
          </div>
        </li>
      ))}
    </ul>
  );
}
