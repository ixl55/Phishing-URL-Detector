import type { LucideIcon } from 'lucide-react';

export function EmptyState({ icon: Icon, text }: { icon: LucideIcon; text: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-12 text-center text-slate-500 dark:text-slate-400">
      <div className="rounded-full bg-slate-100 p-4 dark:bg-slate-800">
        <Icon className="h-6 w-6" aria-hidden />
      </div>
      <p className="text-sm">{text}</p>
    </div>
  );
}
