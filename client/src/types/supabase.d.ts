import type { User } from '@supabase/supabase-js'

declare global {
    interface Window {
        __PINIA_STORES__?: Record<string, any>
    }
}

declare module '@supabase/supabase-js' {
    interface User {
        user_metadata?: {
            avatar_url?: string
            full_name?: string
        }
    }
}