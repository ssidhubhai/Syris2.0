import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          50: '#FDFCFB',
          100: '#F7F6F3',
          200: '#EFECE6',
          300: '#E4DFD5',
        },
        ink: {
          900: '#1A1A1A',
          800: '#2D3134',
          700: '#4A5056',
          500: '#71787E',
          300: '#A1A8AF',
        },
        academic: {
          physics: {
            bg: '#F0F7FF',
            border: '#BAE0FD',
            ink: '#0369A1',
            accent: '#0284C7',
          },
          math: {
            bg: '#F5F3FF',
            border: '#DDD6FE',
            ink: '#6D28D9',
            accent: '#7C3AED',
          },
          chem: {
            bg: '#FFF7ED',
            border: '#FFEDD5',
            ink: '#C2410C',
            accent: '#EA580C',
          }
        },
        kota: {
          trap: '#FEF2F2',
          trapBorder: '#FECACA',
          trapInk: '#991B1B',
        }
      },
      fontFamily: {
        sans: ['system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Georgia', 'Cambria', 'serif'],
        mono: ['Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'paper-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 3px 1px rgba(0, 0, 0, 0.02)',
        'paper-md': '0 2px 4px 0 rgba(0, 0, 0, 0.04), 0 2px 8px 2px rgba(0, 0, 0, 0.03)',
        'paper-glow': '0 0 0 3px rgba(2, 132, 199, 0.25), 0 4px 12px rgba(2, 132, 199, 0.15)',
        'paper-glow-target': '0 0 0 3px rgba(234, 88, 12, 0.35), 0 4px 14px rgba(234, 88, 12, 0.2)',
      }
    },
  },
  plugins: [],
};
export default config;
