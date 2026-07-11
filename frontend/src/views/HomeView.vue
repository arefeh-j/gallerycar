<script setup lang="ts">
import BannerSlider from "../components/BannerSlider.vue";
import StatsSection from "../components/StatsSection.vue";

import HeroSection from "../components/HeroSection.vue";
import CarCard from "../components/CarCard.vue";
import BrandsSection from "../components/BrandsSection.vue";
import FeaturedCars from "../components/FeaturedCars.vue";

import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const brand = ref("");
const year = ref("");

const minPrice = ref("");
const maxPrice = ref("");

function searchCars() {

    router.push({

        path: "/cars",

        query: {

            brand: brand.value,
            year: year.value,
            min: minPrice.value,
            max: maxPrice.value,

        },

    });

}
</script>

<template>

<div class="home">

    <BannerSlider />


    <section class="search-box">

        <h2>جستجوی خودرو</h2>

        <div class="filters">

            <select v-model="brand">

                <option value="">همه برندها</option>
                <option value="BMW">BMW</option>
                <option value="Mercedes">Mercedes</option>
                <option value="Toyota">Toyota</option>
                <option value="Hyundai">Hyundai</option>
                <option value="Kia">Kia</option>

            </select>

            <select v-model="year">

                <option value="">سال ساخت</option>
                <option value="1404">1404</option>
                <option value="1403">1403</option>
                <option value="1402">1402</option>
                <option value="1401">1401</option>

            </select>

            <input
                v-model="minPrice"
                type="number"
                placeholder="حداقل قیمت"
            />

            <input
                v-model="maxPrice"
                type="number"
                placeholder="حداکثر قیمت"
            />

            <button @click="searchCars">

                جستجو

            </button>

        </div>

    </section>

    <BrandsSection />
    <FeaturedCars />
    <StatsSection />

    <section class="latest">

        <h2>

            جدیدترین آگهی‌ها

        </h2>

        <div class="cards">

            <CarCard
                v-for="i in 6"
                :key="i"
                :id="i"
                title="BMW 320i"
                :year="1402"
                mileage="۳۵ هزار کیلومتر"
                price="۲,۵۰۰,۰۰۰,۰۰۰ تومان"
                image="https://placehold.co/600x400"
            />

        </div>

    </section>

</div>

</template>

<style scoped>

.home{
direction: rtl;
}

/* Search Box */

.search-box{

max-width:1200px;

margin:-80px auto 0;

position:relative;

z-index:20;

background:white;

padding:30px;

border-radius:18px;

box-shadow:0 15px 35px rgba(0,0,0,.15);

}

.search-box h2{

margin-top:0;
margin-bottom:20px;

}

.filters{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(180px,1fr));

gap:15px;

align-items:end;

}

.filters input,
.filters select{

padding:13px;

border:1px solid #ddd;

border-radius:10px;

font-size:15px;

}

.filters input:focus,
.filters select:focus{

outline:none;

border-color:#2563eb;

}

.filters button{

background:#2563eb;

color:white;

border:none;

border-radius:10px;

cursor:pointer;

font-size:16px;

transition:.25s;

}

.filters button:hover{

background:#1d4ed8;

}

/* Latest Cars */

.latest{

max-width:1200px;

margin:60px auto;

}

.latest h2{

margin-bottom:25px;

}

.cards{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(320px,1fr));

gap:25px;

}

@media(max-width:900px){

.filters{

grid-template-columns:1fr;

}

.cards{

grid-template-columns:1fr;

}

}

@media (max-width:992px){

.search-box{

margin:30px 20px;

padding:25px;

}

.latest{

margin:40px 20px;

}

}

@media (max-width:768px){

.search-box{

margin:20px 15px;

padding:20px;

border-radius:15px;

}

.search-box h2{

text-align:center;

font-size:22px;

}

.filters{

grid-template-columns:1fr;

}

.filters button{

height:48px;

}

.latest{

margin:35px 15px;

}

.latest h2{

text-align:center;

}

}

@media (max-width:480px){

.search-box{

padding:15px;

}

.filters input,
.filters select,
.filters button{

width:100%;

font-size:14px;

}

}
</style>