import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  email: string;
  password: string; // Добавляем поле для хранения пароля
}

interface AuthState {
  user: User | null;
  login: (email: string, password: string) => void; // Обновляем типизацию функции login
  logout: () => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      login: (email: string, password: string) => {
        set({ user: { email, password } }); // Сохраняем email и пароль
      },
      logout: () => set({ user: null }),
    }),
    {
      name: "auth-storage",
    }
  )
);

export default useAuthStore;
