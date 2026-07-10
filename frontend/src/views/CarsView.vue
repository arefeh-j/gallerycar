<script setup lang="ts">

import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import CarCard from "../components/CarCard.vue";
import { getCars } from "../services/carService";


const route = useRoute();


const cars = ref<any[]>([]);
const loading = ref(true);



function imageUrl(url:string){

    return "http://127.0.0.1:8000" + url;

}



async function loadCars(){

    loading.value = true;


    try{


        const data = await getCars();


        let result = data;



        // برند
        if(route.query.brand){

            result = result.filter(
                (car:any)=>
                car.brand?.name === route.query.brand ||
                car.brand === route.query.brand
            );

        }



        // سال
        if(route.query.year){

            result = result.filter(
                (car:any)=>
                String(car.year) === String(route.query.year)
            );

        }



        // حداقل قیمت
        if(route.query.min){

            result = result.filter(
                (car:any)=>
                car.price >= Number(route.query.min)
            );

        }



        // حداکثر قیمت
        if(route.query.max){

            result = result.filter(
                (car:any)=>
                car.price <= Number(route.query.max)
            );

        }



        cars.value = result;



    }catch(err){

        console.error(err);


    }finally{

        loading.value=false;

    }


}




onMounted(loadCars);



watch(
    ()=>route.query,
    loadCars
);


</script>



<template>


<div class="page">


<h1>
    خودروهای موجود
</h1>



<p class="count">

تعداد خودروها:
{{ cars.length }}

</p>




<div
v-if="loading"
class="loading"
>

در حال بارگذاری...

</div>





<div
v-else-if="cars.length===0"
class="empty"
>

🚗 خودرویی پیدا نشد.

</div>





<div
v-else
class="grid"
>


<CarCard

v-for="car in cars"

:key="car.id"


:id="car.id"


:title="`${car.brand?.name ?? ''} ${car.model ?? ''}`"


:year="car.year"


:mileage="car.mileage"


:price="car.price"


:image="
car.images && car.images.length
?
imageUrl(car.images[0].url)
:
'https://placehold.co/600x400'
"


/>


</div>



</div>


</template>




<style scoped>


.page{

max-width:1200px;

margin:auto;

padding:40px 20px;

direction:rtl;

}



.count{

color:#666;

margin-bottom:25px;

}



.grid{

display:grid;

grid-template-columns:repeat(auto-fill,minmax(320px,1fr));

gap:25px;

}



.loading{

text-align:center;

font-size:20px;

padding:60px;

}



.empty{

text-align:center;

padding:60px;

font-size:20px;

color:#888;

}



</style>