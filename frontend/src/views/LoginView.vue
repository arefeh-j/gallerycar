<script setup lang="ts">
import axios from "axios"
import { useRouter } from "vue-router"
import { ref, computed } from "vue"

const router = useRouter()

const email = ref("")
const password = ref("")
const remember = ref(false)
const showPassword = ref(false)

const emailRegex =
  /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$/;

const emailError = computed(() => {
  if (email.value === "") return "";
  if (!emailRegex.test(email.value))
    return "ایمیل معتبر وارد کنید.";
  return "";
});

const passwordError = computed(() => {
  if (password.value === "") return "";
  if (password.value.length < 8)
    return "رمز عبور باید حداقل ۸ کاراکتر باشد.";
  return "";
});

const isValid = computed(() => {
  return (
    emailRegex.test(email.value) &&
    password.value.length >= 8
  );
});

async function login() {

  try {

    const response = await axios.post(
      "http://127.0.0.1:8000/users/api/login",
      {
        email: email.value,
        password: password.value
      }
    )

    localStorage.setItem(
      "token",
      response.data.access_token
    )

    localStorage.setItem(
      "full_name",
      response.data.full_name
    )

    localStorage.setItem(
      "role",
      response.data.role
    )

    alert("ورود با موفقیت انجام شد.")

    router.push("/")

  }

  catch (err:any){

    alert(
      err.response?.data?.detail ??
      "خطا در ورود"
    )

  }

}
</script>

<template>
  <div class="login-page">

    <div class="login-card">

      <h1>ورود به حساب کاربری</h1>

      <p class="subtitle">
        برای ثبت آگهی و مدیریت خودروهای خود وارد شوید.
      </p>

      <form @submit.prevent="login">

        <div class="form-group">

          <label>ایمیل</label>

          <input
            type="email"
            v-model="email"
            placeholder="example@gmail.com"
            maxlength="100"
            required
            :class="{ error: emailError, success: email && !emailError }"
          />

          <small class="hint">
            فقط ایمیل معتبر وارد کنید.
          </small>

          <small class="error-text" v-if="emailError">
            {{ emailError }}
          </small>

        </div>

        <div class="form-group">

          <label>رمز عبور</label>

          <div class="password-box">

            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="حداقل ۸ کاراکتر"
              maxlength="50"
              required
              :class="{ error: passwordError, success: password && !passwordError }"
            />

            <button
              class="toggle"
              type="button"
              @click="showPassword=!showPassword"
            >
              {{ showPassword ? "🙈" : "👁" }}
            </button>

          </div>

          <small class="hint">
            از رمز عبور قوی شامل حروف و اعداد استفاده کنید.
          </small>

          <small
            class="error-text"
            v-if="passwordError"
          >
            {{ passwordError }}
          </small>

        </div>

        <div class="options">

          <label class="remember">

            <input
              type="checkbox"
              v-model="remember"
            />

            مرا به خاطر بسپار

          </label>

          <a href="#">
            رمز عبور را فراموش کرده‌اید؟
          </a>

        </div>

        <button
          class="login-btn"
          :disabled="!isValid"
        >
          ورود
        </button>

      </form>

      <p class="register-link">

        حساب کاربری ندارید؟

        <RouterLink to="/register">
          ثبت نام
        </RouterLink>

      </p>

    </div>

  </div>
</template>

<style scoped>

.login-page{

display:flex;

justify-content:center;

align-items:center;

padding:60px 20px;

direction:rtl;

}

.login-card{

width:100%;

max-width:450px;

background:white;

padding:35px;

border-radius:18px;

box-shadow:0 15px 40px rgba(0,0,0,.08);

}

h1{

margin:0;

margin-bottom:10px;

text-align:center;

}

.subtitle{

text-align:center;

color:#666;

margin-bottom:30px;

}

.form-group{

margin-bottom:22px;

}

label{

display:block;

margin-bottom:8px;

font-weight:bold;

}

input{

width:100%;

padding:13px;

border:1px solid #d5d5d5;

border-radius:10px;

font-size:15px;

transition:.25s;

}

input:focus{

outline:none;

border-color:#2563eb;

}

.success{

border-color:#22c55e;

}

.error{

border-color:#ef4444;

}

.password-box{

position:relative;

}

.toggle{

position:absolute;

left:10px;

top:50%;

transform:translateY(-50%);

border:none;

background:none;

cursor:pointer;

font-size:18px;

}

.hint{

display:block;

margin-top:6px;

color:#777;

font-size:12px;

}

.error-text{

display:block;

margin-top:6px;

color:#ef4444;

font-size:13px;

}

.options{

display:flex;

justify-content:space-between;

align-items:center;

margin:20px 0;

font-size:14px;

}

.options a{

text-decoration:none;

color:#2563eb;

}

.remember{

display:flex;

gap:8px;

align-items:center;

}

.remember input{

width:auto;

}

.login-btn{

width:100%;

padding:14px;

border:none;

background:#2563eb;

color:white;

font-size:16px;

border-radius:10px;

cursor:pointer;

transition:.25s;

}

.login-btn:hover{

background:#1d4ed8;

}

.login-btn:disabled{

background:#bfc7d7;

cursor:not-allowed;

}

.register-link{

margin-top:25px;

text-align:center;

}

.register-link a{

text-decoration:none;

font-weight:bold;

color:#2563eb;

}

</style>