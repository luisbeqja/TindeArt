import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../utils/supabase'

// Import components
import User from '../views/User.vue'
import Login from '../views/Login.vue'
import Explore from '../views/explore/Explore.vue'


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
            path: '/explore',
            name: 'Explore',
            component: Explore,
            meta: { requiresAuth: false }
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
            meta: { requiresAuth: false }
        },
        {
            path: '/',
            redirect: '/explore'
        }
    ]
})

// Navigation Guard
router.beforeEach(async (to) => {
    const { data: { user } } = await supabase.auth.getUser()

    // Redirect to login if route requires auth and no user
    if (to.meta.requiresAuth && !user) {
        return { name: 'Login' }
    }

    // Redirect to explore if logged-in user tries to access login
    if (to.name === 'Login' && user) {
        return { name: 'Explore' }
    }
})

export default router