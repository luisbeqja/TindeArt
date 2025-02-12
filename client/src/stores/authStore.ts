import { defineStore } from 'pinia'
import { supabase } from '../utils/supabase'

interface AuthState {
    user: any | null
    isLoading: boolean
    error: string | null
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        isLoading: false,
        error: null
    }),

    actions: {
        async initializeAuth() {
            try {
                this.isLoading = true
                const { data: { user } } = await supabase.auth.getUser()
                this.user = user

                supabase.auth.onAuthStateChange((_, session) => {
                    this.user = session?.user || null
                })
            } catch (error) {
                this.error = error instanceof Error ? error.message : 'Auth error'
            } finally {
                this.isLoading = false
            }
        },
    },

    getters: {
        isAuthenticated: (state) => !!state.user
    },

    // CORRECTED PERSIST CONFIG
    persist: {
        strategies: [
            {
                key: 'artmatch-auth',
                storage: localStorage,
                paths: ['user'] // Persist only the `user` state
            }
        ]
    }
})