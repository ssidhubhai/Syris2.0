import type { Metadata } from 'next';
import './globals.css';
import 'katex/dist/katex.min.css';

export const metadata: Metadata = {
  title: 'AI JEE Study Companion — Digital Paper Workspace',
  description: 'Adaptive Digital Study Sheet transforming AI reasoning into structured master solutions.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased font-sans bg-paper-100 text-ink-900 selection:bg-academic-physics-border selection:text-academic-physics-ink">
        {children}
      </body>
    </html>
  );
}
