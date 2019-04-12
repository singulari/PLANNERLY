import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import home from '@/components/home'
import dashboard from '@/components/dashboard'
import questions from '@/components/questions'
import enrolment from '@/components/enrolment'
import distribution from '@/components/distribution'
Vue.use(Router)

let router = new Router({
    routes: [{
        path: '/login',
        name: 'login',
        component: login
    }, {
        path: '/home',
        name: 'home',
        component: home,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem('tokens') == null || localStorage.getItem('tokens') == '') {
                next({
                    path: '/login',
                    query: { redirect: to.fullPath }
                })
            } else {
                next()
            }
        },
        children: [{
            path: '/questions',
            component: questions
        }, {
            path: '/dashboard',
            component: dashboard
        }, {
            path: '/enrolment',
            component: enrolment
        }, {
            path: '/distribution',
            component: distribution
        }]
    }]
})

export default router