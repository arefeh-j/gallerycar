<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";

import CarCard from "../components/CarCard.vue";
import { getCars } from "../services/carService";


const route = useRoute();


const cars = ref<any[]>([]);
const loading = ref(true);

const currentPage = ref(1);
const itemsPerPage = 6;



function imageUrl(url: string) {
  return "http://127.0.0.1:8000" + url;
}



async function loadCars() {

  loading.value = true;

  try {

    const data = await getCars();

    let result = data;


    // Filter Brand
    if (route.query.brand) {

      result = result.filter(
        (car:any)=>
          car.brand?.name === route.query.brand ||
          car.brand === route.query.brand
      );

    }


    // Filter Year
    if(route.query.year){

      result = result.filter(
        (car:any)=>
          String(car.year) === String(route.query.year)
      );

    }


    // Minimum Price
    if(route.query.min){

      result = result.filter(
        (car:any)=>
          car.price >= Number(route.query.min)
      );

    }



    // Maximum Price
    if(route.query.max){

      result = result.filter(
        (car:any)=>
          car.price <= Number(route.query.max)
      );

    }



    cars.value = result;

    currentPage.value = 1;



  }catch(error){

    console.error(error);

  }finally{

    loading.value = false;

  }

}



onMounted(loadCars);



watch(
  ()=>route.query,
  loadCars
);



const totalPages = computed(()=>{

  return Math.ceil(
    cars.value.length / itemsPerPage
  );

});



const paginatedCars = computed(()=>{


  const start =
    (currentPage.value - 1) * itemsPerPage;


  return cars.value.slice(
    start,
    start + itemsPerPage
  );


});



function nextPage(){

  if(currentPage.value < totalPages.value){

    currentPage.value++;

  }

}



function prevPage(){

  if(currentPage.value > 1){

    currentPage.value--;

  }

}


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



<!-- Loading -->

<div
v-if="loading"
class="loading"
>

<div class="spinner"></div>

<p>
در حال بارگذاری خودروها...
</p>

</div>




<!-- Empty -->

<div
v-else-if="cars.length === 0"
class="empty"
>


<div class="empty-icon">
🚗
</div>


<h2>
خودرویی پیدا نشد
</h2>


<p>
فیلترهای جستجو را تغییر دهید یا بعداً دوباره امتحان کنید.
</p>


</div>





<!-- Cars -->

<template v-else>


<div class="grid">


<CarCard

v-for="car in paginatedCars"

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





<!-- Pagination -->


<div
v-if="totalPages > 1"
class="pagination"
>



<button
@click="prevPage"
:disabled="currentPage === 1"
>

قبلی

</button>




<span>

صفحه {{ currentPage }}
از
{{ totalPages }}

</span>




<button
@click="nextPage"
:disabled="currentPage === totalPages"
>

بعدی

</button>



</div>



</template>



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
grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
gap:25px;

}





.loading{

display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
padding:60px;
font-size:20px;

}




.spinner{

width:60px;
height:60px;

border:6px solid #ddd;
border-top:6px solid #2563eb;

border-radius:50%;

animation:spin .8s linear infinite;

margin-bottom:20px;

}



@keyframes spin{

from{

transform:rotate(0deg);

}

to{

transform:rotate(360deg);

}

}




.empty{

text-align:center;
padding:70px 20px;

}




.empty-icon{

font-size:70px;
margin-bottom:15px;

}




.empty h2{

color:#444;

}




.empty p{

color:#777;
font-size:17px;

}





.pagination{

display:flex;
justify-content:center;
align-items:center;
gap:20px;
margin-top:40px;
flex-wrap:wrap;

}



.pagination button{

background:#2563eb;
color:white;

border:none;

padding:10px 18px;

border-radius:8px;

cursor:pointer;

}



.pagination button:disabled{

background:#cbd5e1;

cursor:not-allowed;

}



.pagination span{

font-weight:bold;

}





@media(max-width:768px){


.grid{

grid-template-columns:1fr;

}


.page h1{

text-align:center;

}


.pagination button{

padding:8px 14px;

}


}



</style>