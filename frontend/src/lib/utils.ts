import type { Severity, Verdict } from './types';

export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(' ');
}

export const verdictStyles: Record<
  Verdict,
  { text: string; bg: string; border: string; ring: string; stroke: string; soft: string }
> = {
  safe: {
    text: 'text-emerald-700 dark:text-emerald-300',
    bg: 'bg-emerald-600',
    border: 'border-emerald-200 dark:border-emerald-900',
    ring: 'ring-emerald-500/20',
    stroke: '#059669',
    soft: 'bg-emerald-50 dark:bg-emerald-950/40',
  },
  suspicious: {
    text: 'text-amber-700 dark:text-amber-300',
    bg: 'bg-amber-500',
    border: 'border-amber-200 dark:border-amber-900',
    ring: 'ring-amber-500/20',
    stroke: '#d97706',
    soft: 'bg-amber-50 dark:bg-amber-950/40',
  },
  dangerous: {
    text: 'text-red-700 dark:text-red-300',
    bg: 'bg-red-600',
    border: 'border-red-200 dark:border-red-900',
    ring: 'ring-red-500/20',
    stroke: '#dc2626',
    soft: 'bg-red-50 dark:bg-red-950/40',
  },
};

export const severityStyles: Record<Severity, string> = {
  high: 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300',
  medium: 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300',
  low: 'bg-sky-100 text-sky-700 dark:bg-sky-950 dark:text-sky-300',
};

export function formatDate(iso: string, lang: string): string {
  const date = new Date(iso.endsWith('Z') || iso.includes('+') ? iso : `${iso}Z`);
  return new Intl.DateTimeFormat(lang === 'ar' ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}
