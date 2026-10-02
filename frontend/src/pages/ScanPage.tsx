import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ShieldHalf } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { ResultCard } from '../components/scan/ResultCard';
import { UrlInput } from '../components/scan/UrlInput';
import { Alert } from '../components/ui/Alert';
import { ApiError, api } from '../lib/api';
import type { Lang } from '../lib/types';

export function ScanPage() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language as Lang;
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: api.analyzeUrl,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
  });

  const error = mutation.error;
  const errorText =
    error instanceof ApiError && error.localized ? error.localized[lang] : t('scan.error');

  return (
    <div className="space-y-8">
      <section className="space-y-4 pt-4 text-center">
        <div className="mx-auto inline-flex rounded-2xl bg-brand-50 p-3 text-brand-600 dark:bg-brand-950 dark:text-brand-400">
          <ShieldHalf className="h-8 w-8" aria-hidden />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl dark:text-white">
          {t('scan.title')}
        </h1>
        <p className="mx-auto max-w-2xl text-slate-600 dark:text-slate-400">{t('scan.subtitle')}</p>
      </section>

      <UrlInput loading={mutation.isPending} onSubmit={(url) => mutation.mutate(url)} />

      {mutation.isError && <Alert>{errorText}</Alert>}
      {mutation.data && !mutation.isPending && (
        <ResultCard key={mutation.data.normalized_url} result={mutation.data} />
      )}
    </div>
  );
}
