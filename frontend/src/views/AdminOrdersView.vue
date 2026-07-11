<template>

<div class="container">

<h1>درخواست‌های خرید</h1>

<table>

<thead>

<tr>

<th>نام کاربر</th>

<th>شماره تماس</th>

<th>خودرو</th>

<th>تاریخ</th>

<th>وضعیت</th>

</tr>

</thead>

<tbody>

<tr
v-for="order in orders"
:key="order.id"
>

<td>{{ order.user }}</td>

<td>{{ order.phone }}</td>

<td>{{ order.car }}</td>

<td>{{ order.created_at }}</td>

<td>

<select
v-model="order.status"
@change="changeStatus(order)"
>

<option value="pending">

در انتظار

</option>

<option value="called">

تماس گرفته شد

</option>

<option value="completed">

تکمیل شد

</option>

</select>

</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup lang="ts">

import {ref,onMounted} from "vue";

import axios from "axios";

const orders=ref<any[]>([]);

async function loadOrders(){

const token=localStorage.getItem("token");

const res=await axios.get(

"http://127.0.0.1:8000/orders/api/admin",

{

headers:{

Authorization:`Bearer ${token}`

}

}

);

orders.value=res.data;

}

async function changeStatus(order:any){

const token=localStorage.getItem("token");

await axios.put(

`http://127.0.0.1:8000/orders/api/${order.id}`,

{

status:order.status

},

{

headers:{

Authorization:`Bearer ${token}`

}

}

);

}

onMounted(loadOrders);

</script>

<style scoped>

.container{

max-width:1200px;

margin:auto;

padding:30px;

direction:rtl;

}

table{

width:100%;

border-collapse:collapse;

}

th,td{

padding:15px;

border-bottom:1px solid #ddd;

text-align:center;

}

select{

padding:8px;

border-radius:8px;

}

</style>