/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  safelist: [],
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./accounts/templates/**/*.html",
    "./exams/templates/**/*.html",
    "./plan/templates/**/*.html",
    "./notify/templates/**/*.html",

    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // Design System Colors (Cognitive Catalyst)
        indigo: {
          DEFAULT: '#1c0070',
          dark: '#311b92',
          light: '#3d2780',
        },
        amber: {
          DEFAULT: '#feb300',
          dark: '#e5a100',
          light: '#ffc41f',
        },
        teal: {
          DEFAULT: '#8df5e4',
          dark: '#70d8c8',
          dim: '#002420',
        },
        surface: {
          base: '#fdf8fd',
          low: '#f7f2f8',
          high: '#ebe7ec',
          card: '#ffffff',
        },
        body: {
          DEFAULT: '#1c1b1f',
          secondary: '#474553',
        },
        // Keep existing primary palette for compatibility
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
          950: "#172554",
        },
      },
      boxShadow: {
        'card': '0px 4px 20px rgba(28, 27, 31, 0.04)',
        'card-hover': '0px 8px 30px rgba(28, 27, 31, 0.08)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'fade-in-up': 'fadeInUp 0.8s ease-out',
        'slide-in-left': 'slideInLeft 0.8s ease-out',
        'slide-in-right': 'slideInRight 0.8s ease-out',
        'pulse-slow': 'pulse 3s infinite',
        'bounce-slow': 'bounce 2s infinite',
    },
    keyframes: {
      float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
      },
      fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
      },
      slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
      },
      slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
      }
    }
    },
  },
  plugins: [
    require("flowbite/plugin")({
      charts: true,
      datatables: true,
    }),
  ],
};
