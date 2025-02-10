import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../utils/supabase'

// Import components
import User from '../views/User.vue'
import Login from '../views/Login.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/profile',
            name: 'Profile',
            component: User,
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
            meta: { requiresAuth: false }
        },
    ]
})

// Navigation Guard
router.beforeEach(async (to) => {
    const { data: { user } } = await supabase.auth.getUser()

    // Redirect to login if route requires auth and no user
    if (to.meta.requiresAuth && !user) {
        return { name: 'Login' }
    }

    // Redirect to swipe if logged-in user tries to access login
    if (to.name === 'Login' && user) {
        return { name: 'User' }
    }
})

export default router