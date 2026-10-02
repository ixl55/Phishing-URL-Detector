import { History, Layers, ShieldAlert, Search } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { cn } from '../../lib/utils';
import { LanguageToggle } from './LanguageToggle';
import { ThemeToggle } from './ThemeToggle';

const links = [
  { to: '/', key: 'nav.scan', icon: Search },
  { to: '/batch', key: 'nav.batch', icon: Layers },
  { to: '/history', key: 'nav.history', icon: History },
] as const;

export function Navbar() {
  const { t } = useTranslation();
  return (
    <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3">
        <NavLink
          to="/"
          className="flex items-center gap-2 font-semibold text-slate-900 dark:text-white"
        >
          <span className="rounded-lg bg-brand-600 p-1.5 text-white">
            <ShieldAlert className="h-5 w-5" aria-hidden />
          </span>
          <span>{t('app.name')}</span>
        </NavLink>

        <nav className="order-3 flex w-full gap-1 sm:order-none sm:w-auto">
          {links.map(({ to, key, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-brand-50 text-brand-700 dark:bg-brand-950 dark:text-brand-300'
                    : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800',
                )
              }
            >
              <Icon className="h-4 w-4" aria-hidden />
              {t(key)}
            </NavLink>
          ))}
        </nav>

        <div className="ms-auto flex items-center gap-1">
          <LanguageToggle />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
