/// <reference types="vite/client" />

import 'pinia-plugin-persistedstate'

declare module 'pinia' {
    export interface DefineStoreOptionsBase<S, Store> {
        persist?: boolean | PersistedStateOptions
    }
}

interface PersistedStateOptions {
    key?: string
    storage?: 'local' | 'session'
    paths?: string[]
}