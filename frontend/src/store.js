import { create } from 'zustand';

export const useStore = create((set) => ({
  darkMode: true,
  toggleDarkMode: () => set((s) => ({ darkMode: !s.darkMode })),
}));
