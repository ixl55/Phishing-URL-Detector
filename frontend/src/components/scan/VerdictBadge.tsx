import { ShieldAlert, ShieldCheck, ShieldQuestion } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Verdict } from '../../lib/types';
import { cn, verdictStyles } from '../../lib/utils';

const icons = { safe: ShieldCheck, suspicious: ShieldQuestion, dangerous: ShieldAlert };

export function VerdictBadge({ verdict, size = 'md' }: { verdict: Verdict; size?: 'sm' | 'md' }) {
  const { t } = useTranslation();
  const Icon = icons[verdict];
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full font-semibold text-white',
        verdictStyles[verdict].bg,
        size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm',
      )}
    >
      <Icon className={size === 'sm' ? 'h-3.5 w-3.5' : 'h-4 w-4'} aria-hidden />
      {t(`verdict.${verdict}`)}
    </span>
  );
}
