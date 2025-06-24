import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import AdminHome from '@/components/AdminHome.vue'
import LogOut from '@/components/Logout.vue'
import CustomerPage from '@/components/CustomerPage.vue'
import ProfessionalPage from '@/components/ProfessionalPage.vue'
import AllUsers from '@/components/AllUsers.vue'
import ServicesPage from '@/components/ServicesPage.vue'
import ProfessionalRequests from '@/components/ProfessionalRequests.vue'
import AddNewService from '@/components/AddNewService.vue'
import SearchServices from '@/components/SearchServices.vue'
import MyServiceRequests from '@/components/MyServiceRequests.vue'
import ProfServiceRequest from '@/components/ProfServiceRequest.vue'
import AdminHomePage from '@/components/AdminHomePage.vue'
import CustomerHome from '@/components/CustomerHome.vue'
import ProfessionalHome from '@/components/ProfessionalHome.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminHome,
    children:[
      {
        path: 'home',
        component: AdminHomePage
      },
      {
        path: 'allusers',
        component: AllUsers
      },
      {
        path: 'services',
        component: ServicesPage,
        children:[
          {
            path: 'addnewservice',
            component: AddNewService
          }
        ]
      },
      {
        path: 'requests',
        component: ProfessionalRequests
      }
    ]
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogOut
  },
  {
    path: '/customer',
    name: 'customer',
    component: CustomerPage,
    children:[
      {
        path: 'home',
        component: CustomerHome
      },
      {
        path: 'searchservices',
        component: SearchServices
      },
      {
        path: 'myservicerequests',
        component: MyServiceRequests
      }
    ]
  },
  {
    path: '/professional',
    name: 'professional',
    component: ProfessionalPage,
    children:[
      {
        path: 'home',
        component: ProfessionalHome
      },
      {
        path: 'myservicerequests',
        component: ProfServiceRequest
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
