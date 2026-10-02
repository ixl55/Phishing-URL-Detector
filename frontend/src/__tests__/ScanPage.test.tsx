import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ScanPage } from '../pages/ScanPage';
import { dangerousResult } from './fixtures';

function renderPage() {
  const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <ScanPage />
    </QueryClientProvider>,
  );
}

describe('ScanPage', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('submits the URL and renders the result', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(JSON.stringify(dangerousResult), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      );
    vi.stubGlobal('fetch', fetchMock);

    renderPage();
    await userEvent.type(
      screen.getByPlaceholderText('https://example.com/login'),
      'http://paypal.com@evil.tk/login',
    );
    await userEvent.click(screen.getByRole('button', { name: /افحص/ }));

    expect(await screen.findByTestId('result-card')).toHaveAttribute('data-verdict', 'dangerous');
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/analyze',
      expect.objectContaining({ method: 'POST' }),
    );
  });

  it('shows the localized server error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: {
              code: 'invalid',
              message: { ar: 'هذا لا يبدو رابطاً صالحاً.', en: 'Invalid' },
            },
          }),
          {
            status: 422,
          },
        ),
      ),
    );

    renderPage();
    await userEvent.type(screen.getByPlaceholderText('https://example.com/login'), 'nope nope');
    await userEvent.click(screen.getByRole('button', { name: /افحص/ }));

    expect(await screen.findByRole('alert')).toHaveTextContent('هذا لا يبدو رابطاً صالحاً.');
  });
});
