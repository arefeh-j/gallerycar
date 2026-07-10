import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import CarsView from "../views/CarsView.vue";
import CarDetailsView from "../views/CarDetailsView.vue";
import AddCarView from "../views/AddCarView.vue";
import EditCarView from "../views/EditCarView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import FavoritesView from "../views/FavoritesView.vue";
import AdminView from "../views/AdminView.vue";

import ProfileView from "../views/ProfileView.vue";

const router = createRouter({

  history: createWebHistory(),

  routes: [

    {
    path: "/profile",
    name: "profile",
    component: ProfileView,
    meta:{
        requiresAuth:true
    }
    },

    {
      path: "/",
      name: "home",
      component: HomeView,
    },


    {
      path: "/cars",
      name: "cars",
      component: CarsView,
    },


    {
      path: "/cars/add",
      name: "add-car",
      component: AddCarView,
      meta: {
        requiresAuth: true
      }
    },


    {
      path: "/cars/edit/:id",
      name: "edit-car",
      component: EditCarView,
      meta: {
        requiresAuth: true
      }
    },


    // صفحه جزئیات خودرو
    {
      path: "/cars/:id",
      name: "car-details",
      component: CarDetailsView,
    },


    {
      path: "/login",
      name: "login",
      component: LoginView,
    },


    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },


    {
      path: "/favorites",
      name: "favorites",
      component: FavoritesView,
      meta: {
        requiresAuth: true
      }
    },


    {
      path: "/admin",
      name: "admin",
      component: AdminView,
      meta: {
        requiresAuth: true,
        requiresAdmin: true
      }
    },


  ],

});



// Route Guard

router.beforeEach((to, from, next) => {


  const token = localStorage.getItem("token");

  const role = localStorage.getItem("role");



  if (to.meta.requiresAuth && !token) {

    next("/login");

  }


  else if (to.meta.requiresAdmin && role !== "admin") {

    next("/");

  }


  else {

    next();

  }


});



export default router;