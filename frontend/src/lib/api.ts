import type { Analysis, BatchResponse, HistoryPage, LocalizedText, Stats, Verdict } from './types';

export class ApiError extends Error {
  constructor(
    public status: number,
    public localized: LocalizedText | null,
  ) {
    super(localized?.en ?? `Request failed (${status})`);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  });
  if (!response.ok) {
    let localized: LocalizedText | null = null;
    try {
      const body = await response.json();
      if (body?.detail?.message?.ar) localized = body.detail.message;
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(response.status, localized);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  analyzeUrl: (url: string) =>
    request<Analysis>('/api/analyze', { method: 'POST', body: JSON.stringify({ url }) }),

  analyzeBatch: (text: string) =>
    request<BatchResponse>('/api/analyze/batch', {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),

  getHistory: (params: { limit: number; offset: number; verdict?: Verdict | '' }) => {
    const query = new URLSearchParams({
      limit: String(params.limit),
      offset: String(params.offset),
    });
    if (params.verdict) query.set('verdict', params.verdict);
    return request<HistoryPage>(`/api/history?${query}`);
  },

  deleteScan: (id: number) => request<void>(`/api/history/${id}`, { method: 'DELETE' }),

  clearHistory: () => request<{ deleted: number }>('/api/history', { method: 'DELETE' }),

  getStats: () => request<Stats>('/api/stats'),
};
