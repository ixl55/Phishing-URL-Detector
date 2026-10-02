import { useTranslation } from 'react-i18next';
import type { Analysis } from '../../lib/types';
import { cn } from '../../lib/utils';

/** Shows the URL split into its parts; the registered domain (the part that decides who owns the site) is highlighted. */
export function UrlBreakdown({ result }: { result: Analysis }) {
  const { t } = useTranslation();
  const flagged = result.verdict !== 'safe';
  const label = result.suffix
    ? result.registered_domain.slice(0, -(result.suffix.length + 1))
    : result.registered_domain;

  const parts = [
    { key: 'scheme', value: result.scheme ? `${result.scheme}://` : '', tone: 'text-slate-500' },
    {
      key: 'subdomain',
      value: result.subdomain ? `${result.subdomain}.` : '',
      tone: 'text-slate-500',
    },
    {
      key: 'domain',
      value: label,
      tone: flagged
        ? 'rounded bg-red-100 px-1 font-semibold text-red-700 dark:bg-red-950 dark:text-red-300'
        : 'rounded bg-emerald-100 px-1 font-semibold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300',
    },
    {
      key: 'suffix',
      value: result.suffix ? `.${result.suffix}` : '',
      tone: 'text-slate-700 dark:text-slate-300',
    },
    { key: 'path', value: result.path, tone: 'text-slate-400' },
  ].filter((p) => p.value);

  if (!result.host) return null;

  return (
    <div className="space-y-3">
      <p
        dir="ltr"
        className="break-all rounded-xl bg-slate-50 p-3 text-start font-mono text-sm dark:bg-slate-950"
      >
        {parts.map((p) => (
          <span key={p.key} className={p.tone}>
            {p.value}
          </span>
        ))}
      </p>
      <dl className="space-y-2 text-sm">
        {parts.map((p) => (
          <div
            key={p.key}
            className="flex items-baseline justify-between gap-3 border-b border-dashed border-slate-200 pb-1 dark:border-slate-800"
          >
            <dt className="shrink-0 text-slate-500 dark:text-slate-400">
              {t(`result.parts.${p.key}`)}
            </dt>
            <dd
              dir="ltr"
              className={cn('truncate font-mono text-slate-800 dark:text-slate-200')}
              title={p.value}
            >
              {p.value}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
