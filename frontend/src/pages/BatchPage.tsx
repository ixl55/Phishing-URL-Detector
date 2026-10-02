import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { BatchInput } from '../components/batch/BatchInput';
import { BatchResultsTable } from '../components/batch/BatchResultsTable';
import { BatchSummary } from '../components/batch/BatchSummary';
import { Alert } from '../components/ui/Alert';
import { ApiError, api } from '../lib/api';
import type { Lang } from '../lib/types';

export function BatchPage() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language as Lang;
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: api.analyzeBatch,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
  });

  const error = mutation.error;
  const errorText =
    error instanceof ApiError && error.localized ? error.localized[lang] : t('scan.error');

  return (
    <div className="space-y-6">
      <section className="space-y-2">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">{t('batch.title')}</h1>
        <p className="text-slate-600 dark:text-slate-400">{t('batch.subtitle')}</p>
      </section>

      <BatchInput loading={mutation.isPending} onSubmit={(text) => mutation.mutate(text)} />

      {mutation.isError && <Alert>{errorText}</Alert>}
      {mutation.data && !mutation.isPending && (
        <div className="animate-fade-up space-y-4">
          <BatchSummary summary={mutation.data.summary} />
          <BatchResultsTable items={mutation.data.items} />
        </div>
      )}
    </div>
  );
}
