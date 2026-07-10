import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import CarsView from "../views/CarsView.vue";
import CarDetailView from "../views/CarDetailView.vue";
import AddCarView from "../views/AddCarView.vue";
import EditCarView from "../views/EditCarView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import FavoritesView from "../views/FavoritesView.vue";
import AdminView from "../views/AdminView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
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
      path: "/cars/:id",
      name: "car-detail",
      component: CarDetailView,
    },
    {
      path: "/cars/add",
      name: "add-car",
      component: AddCarView,
    },
    {
      path: "/cars/edit/:id",
      name: "edit-car",
      component: EditCarView,
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
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminView,
    },
  ],
});

export default router;