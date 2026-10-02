import { useState } from 'react';
import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { ChevronLeft, ChevronRight, History, Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { HistoryTable } from '../components/history/HistoryTable';
import { RulesChart } from '../components/history/RulesChart';
import { StatsCards } from '../components/history/StatsCards';
import { Alert } from '../components/ui/Alert';
import { Button } from '../components/ui/Button';
import { Card, CardTitle } from '../components/ui/Card';
import { EmptyState } from '../components/ui/EmptyState';
import { Spinner } from '../components/ui/Spinner';
import { api } from '../lib/api';
import type { Verdict } from '../lib/types';
import { cn } from '../lib/utils';

const PAGE_SIZE = 10;
const FILTERS: (Verdict | '')[] = ['', 'safe', 'suspicious', 'dangerous'];

export function HistoryPage() {
  const { t, i18n } = useTranslation();
  const queryClient = useQueryClient();
  const [verdict, setVerdict] = useState<Verdict | ''>('');
  const [page, setPage] = useState(0);

  const stats = useQuery({ queryKey: ['stats'], queryFn: api.getStats });
  const history = useQuery({
    queryKey: ['history', verdict, page],
    queryFn: () => api.getHistory({ limit: PAGE_SIZE, offset: page * PAGE_SIZE, verdict }),
    placeholderData: keepPreviousData,
  });

  const refresh = () => {
    queryClient.invalidateQueries({ queryKey: ['history'] });
    queryClient.invalidateQueries({ queryKey: ['stats'] });
  };
  const remove = useMutation({ mutationFn: api.deleteScan, onSuccess: refresh });
  const clear = useMutation({
    mutationFn: api.clearHistory,
    onSuccess: () => {
      setPage(0);
      refresh();
    },
  });

  const total = history.data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const isRtl = i18n.dir() === 'rtl';
  const PrevIcon = isRtl ? ChevronRight : ChevronLeft;
  const NextIcon = isRtl ? ChevronLeft : ChevronRight;

  return (
    <div className="space-y-6">
      <section className="flex flex-wrap items-end justify-between gap-3">
        <div className="space-y-2">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            {t('history.title')}
          </h1>
          <p className="text-slate-600 dark:text-slate-400">{t('history.subtitle')}</p>
        </div>
        <Button
          variant="danger"
          size="sm"
          disabled={!stats.data?.total || clear.isPending}
          onClick={() => window.confirm(t('history.confirmClear')) && clear.mutate()}
        >
          <Trash2 className="h-4 w-4" aria-hidden />
          {t('history.clear')}
        </Button>
      </section>

      {(stats.isError || history.isError) && <Alert>{t('scan.error')}</Alert>}

      {stats.data && <StatsCards stats={stats.data} />}

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <span className="text-sm text-slate-500 dark:text-slate-400">
              {t('history.filter')}:
            </span>
            {FILTERS.map((f) => (
              <button
                key={f || 'all'}
                type="button"
                onClick={() => {
                  setVerdict(f);
                  setPage(0);
                }}
                className={cn(
                  'rounded-full px-3 py-1 text-xs font-medium transition-colors',
                  verdict === f
                    ? 'bg-brand-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700',
                )}
              >
                {f ? t(`verdict.${f}`) : t('history.all')}
              </button>
            ))}
            {history.isFetching && <Spinner className="ms-auto text-slate-400" />}
          </div>

          {history.data && history.data.items.length > 0 ? (
            <>
              <HistoryTable scans={history.data.items} onDelete={(id) => remove.mutate(id)} />
              {pages > 1 && (
                <div className="mt-4 flex items-center justify-between text-sm">
                  <Button
                    variant="secondary"
                    size="sm"
                    disabled={page === 0}
                    onClick={() => setPage((p) => p - 1)}
                  >
                    <PrevIcon className="h-4 w-4" aria-hidden />
                    {t('history.prev')}
                  </Button>
                  <span className="text-slate-500">
                    {t('history.page', { page: page + 1, pages })}
                  </span>
                  <Button
                    variant="secondary"
                    size="sm"
                    disabled={page + 1 >= pages}
                    onClick={() => setPage((p) => p + 1)}
                  >
                    {t('history.next')}
                    <NextIcon className="h-4 w-4" aria-hidden />
                  </Button>
                </div>
              )}
            </>
          ) : (
            !history.isLoading && <EmptyState icon={History} text={t('history.empty')} />
          )}
        </Card>

        <Card>
          <CardTitle>{t('history.topRules')}</CardTitle>
          {stats.data && stats.data.top_rules.length > 0 ? (
            <RulesChart rules={stats.data.top_rules} />
          ) : (
            <EmptyState icon={History} text={t('history.empty')} />
          )}
        </Card>
      </div>
    </div>
  );
}
