<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  getProfile,
  updateProfile
} from "../services/profileService";
import { useRouter } from "vue-router";

const router = useRouter();
const loading = ref(true);
const saving = ref(false);

const form = ref({
  full_name: "",
  email: "",
  phone: "",
  password: ""
});

const message = ref("");

onMounted(async () => {
  try {
    const user = await getProfile();

    form.value.full_name = user.full_name;
    form.value.email = user.email;
    form.value.phone = user.phone || "";

  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
});

async function saveProfile() {

  saving.value = true;
  message.value = "";

  try {

    await updateProfile(form.value);

    localStorage.setItem("full_name", form.value.full_name);

    router.push("/");

  } catch (error) {

    console.log(error);
    message.value = "❌ خطا در ذخیره اطلاعات.";

  } finally {

    saving.value = false;

  }
}
</script>

<template>

<div class="page">
<h1 style="color:red">PROFILE TEST</h1>

<h1>پروفایل کاربر</h1>

<div v-if="loading">
در حال بارگذاری...
</div>

<div v-else>

<div class="form">

<label>نام</label>

<input
v-model="form.full_name"
type="text"
/>

<label>ایمیل</label>

<input
v-model="form.email"
type="email"
/>

<label>شماره تلفن</label>

<input
v-model="form.phone"
type="text"
/>

<label>رمز عبور جدید (اختیاری)</label>

<input
v-model="form.password"
type="password"
/>

<button
@click="saveProfile"
:disabled="saving"
>

{{ saving ? "در حال ذخیره..." : "ذخیره تغییرات" }}

</button>

<p class="message">
{{ message }}
</p>

</div>

</div>

</div>

</template>

<style scoped>

.page{
    max-width:600px;
    margin:auto;
    padding:40px;
}

.form{
    display:flex;
    flex-direction:column;
    gap:15px;
}

input{
    padding:12px;
    border:1px solid #ddd;
    border-radius:8px;
    font-size:15px;
}

button{
    padding:12px;
    border:none;
    border-radius:8px;
    background:#2563eb;
    color:white;
    cursor:pointer;
    font-size:16px;
}

button:disabled{
    opacity:.6;
    cursor:not-allowed;
}

.message{
    margin-top:10px;
    font-weight:bold;
}

</style>