/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nebula: {
          background: '#0b1323',
          surface: '#0b1323',
          on_surface: '#dbe2f8',
          on_surface_variant: '#bac9cc',
          primary: '#c3f5ff',
          primary_container: '#00e5ff',
          on_primary: '#00363d',
          surface_container_lowest: '#060e1d',
          surface_container_low: '#131c2b',
          surface_container: '#18202f',
          surface_container_high: '#222a3a',
          surface_container_highest: '#2d3546',
          surface_variant: '#2d3546',
          outline: '#849396',
          outline_variant: '#3b494c',
          error: '#ffb4ab',
          error_container: '#93000a',
          on_error: '#690005',
          on_error_container: '#ffdad6',
          primary_fixed: '#9cf0ff',
          primary_fixed_dim: '#00daf3',
        }
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
        mono: ['Manrope', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'fade-slide': 'fadeSlide 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeSlide: {
          '0%': { transform: 'translateY(4px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
