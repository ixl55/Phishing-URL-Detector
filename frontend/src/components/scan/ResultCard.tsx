import { useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Analysis, Lang } from '../../lib/types';
import { cn, verdictStyles } from '../../lib/utils';
import { Card, CardTitle } from '../ui/Card';
import { FindingsList } from './FindingsList';
import { RiskGauge } from './RiskGauge';
import { UrlBreakdown } from './UrlBreakdown';
import { VerdictBadge } from './VerdictBadge';

export function ResultCard({ result }: { result: Analysis }) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language as Lang;
  const style = verdictStyles[result.verdict];
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(result.normalized_url);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard unavailable */
    }
  };

  return (
    <div
      className="animate-fade-up space-y-4"
      data-testid="result-card"
      data-verdict={result.verdict}
    >
      <div
        className={cn(
          'overflow-hidden rounded-2xl border shadow-sm ring-4',
          style.border,
          style.ring,
          style.soft,
        )}
      >
        <div className={cn('h-1.5', style.bg)} />
        <div className="flex flex-col items-center gap-6 p-6 sm:flex-row">
          <RiskGauge score={result.score} verdict={result.verdict} />
          <div className="min-w-0 flex-1 space-y-3 text-center sm:text-start">
            <VerdictBadge verdict={result.verdict} />
            <p className={cn('text-lg font-semibold leading-snug', style.text)}>
              {result.advice[lang]}
            </p>
            <div className="flex items-center justify-center gap-2 sm:justify-start">
              <code
                dir="ltr"
                className="truncate rounded-lg bg-white/70 px-2 py-1 font-mono text-xs text-slate-600 dark:bg-slate-900/70 dark:text-slate-300"
              >
                {result.normalized_url}
              </code>
              <button
                type="button"
                onClick={copy}
                className="shrink-0 rounded-lg p-1.5 text-slate-500 hover:bg-white/70 dark:hover:bg-slate-900/70"
                aria-label={copied ? t('result.copied') : t('result.copy')}
                title={copied ? t('result.copied') : t('result.copy')}
              >
                {copied ? (
                  <Check className="h-4 w-4 text-emerald-600" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <CardTitle>
            {t('result.reasons')} <span className="text-slate-400">({result.findings.length})</span>
          </CardTitle>
          <FindingsList findings={result.findings} />
        </Card>
        <Card className="lg:col-span-2">
          <CardTitle>{t('result.breakdown')}</CardTitle>
          <UrlBreakdown result={result} />
        </Card>
      </div>
    </div>
  );
}
