import { Info } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export function Footer() {
  const { t } = useTranslation();
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800">
      <div className="mx-auto flex max-w-5xl flex-col gap-1 px-4 py-6 text-xs text-slate-500 dark:text-slate-400">
        <p className="flex items-start gap-2">
          <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
          {t('footer.disclaimer')}
        </p>
        <p className="ps-5">{t('footer.privacy')}</p>
      </div>
    </footer>
  );
}
