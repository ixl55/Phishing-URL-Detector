import { useState, type FormEvent } from 'react';
import { Link2, ScanSearch } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../ui/Button';
import { Spinner } from '../ui/Spinner';

const EXAMPLES = [
  'https://www.google.com',
  'http://paypal.com@login-verify.tk/signin',
  'https://alrajhi-online.top/update/account',
  'http://xn--pple-43d.com',
  'https://bit.ly/3xYzAbC',
];

interface Props {
  loading: boolean;
  onSubmit: (url: string) => void;
}

export function UrlInput({ loading, onSubmit }: Props) {
  const { t } = useTranslation();
  const [value, setValue] = useState('');

  const submit = (event: FormEvent) => {
    event.preventDefault();
    if (value.trim()) onSubmit(value.trim());
  };

  const tryExample = (url: string) => {
    setValue(url);
    onSubmit(url);
  };

  return (
    <div className="space-y-3">
      <form onSubmit={submit} className="flex flex-col gap-2 sm:flex-row">
        <label className="relative flex-1">
          <span className="sr-only">URL</span>
          <Link2
            className="pointer-events-none absolute start-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
            aria-hidden
          />
          <input
            type="text"
            dir="ltr"
            inputMode="url"
            autoComplete="off"
            spellCheck={false}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder={t('scan.placeholder')}
            className="w-full rounded-xl border border-slate-300 bg-white py-3 pe-4 ps-11 font-mono text-sm text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
            style={{ textAlign: 'start' }}
          />
        </label>
        <Button type="submit" size="lg" disabled={loading || !value.trim()}>
          {loading ? <Spinner /> : <ScanSearch className="h-5 w-5" aria-hidden />}
          {loading ? t('scan.analyzing') : t('scan.button')}
        </Button>
      </form>

      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-500 dark:text-slate-400">{t('scan.examples')}</span>
        {EXAMPLES.map((url) => (
          <button
            key={url}
            type="button"
            dir="ltr"
            onClick={() => tryExample(url)}
            className="rounded-full border border-slate-200 bg-white px-2.5 py-1 font-mono text-slate-600 transition hover:border-brand-300 hover:text-brand-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-brand-700 dark:hover:text-brand-300"
          >
            {url.replace(/^https?:\/\//, '')}
          </button>
        ))}
      </div>
    </div>
  );
}
