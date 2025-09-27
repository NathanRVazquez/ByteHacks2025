import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref<{ id: string; email: string } | null>(null);
  const isAuthenticated = computed(() => user.value !== null);

  function setUser(userData: { id: string; email: string } | null) {
    user.value = userData;
  }
  async function login(email: string, password: string) {
    return await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    }).then(res => res.json());
  }

  async function signup(email: string, password: string) {
    return await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, created_at: new Date().toISOString() }),
    }).then(res => res.json());
  }

  async function googleSignIn() {
    window.location.href = "http://localhost:8000/google-login";
  }

  return { user, isAuthenticated, login, setUser, signup, googleSignIn };
});