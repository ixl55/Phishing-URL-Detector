import { act, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import i18n from '../i18n';
import { ResultCard } from '../components/scan/ResultCard';
import { dangerousResult, safeResult } from './fixtures';

describe('ResultCard', () => {
  it('shows a dangerous verdict with its reasons in Arabic', () => {
    render(<ResultCard result={dangerousResult} />);
    expect(screen.getByTestId('result-card')).toHaveAttribute('data-verdict', 'dangerous');
    expect(screen.getByText('خطر')).toBeInTheDocument();
    expect(screen.getByText('رمز @ داخل الرابط')).toBeInTheDocument();
    expect(screen.getByRole('meter')).toHaveAttribute('aria-valuenow', '100');
  });

  it('switches texts to English', async () => {
    render(<ResultCard result={dangerousResult} />);
    await act(() => i18n.changeLanguage('en'));
    expect(screen.getByText('Dangerous')).toBeInTheDocument();
    expect(screen.getByText('@ symbol in the address')).toBeInTheDocument();
  });

  it('shows the no-reasons message for safe links', () => {
    render(<ResultCard result={safeResult} />);
    expect(screen.getByText('آمن')).toBeInTheDocument();
    expect(screen.getByText('لم يتم العثور على أي مؤشرات خطر في هذا الرابط.')).toBeInTheDocument();
  });
});
