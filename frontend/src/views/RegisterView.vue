<template>
  <div class="login-page">
    <div class="login-card">
      <h1>ایجاد حساب کاربری</h1>
      <p class="subtitle">برای استفاده از امکانات سایت ثبت نام کنید.</p>

      <form @submit.prevent="register">
        <div class="form-group">
          <label>نام کامل</label>
          <input
            type="text"
            v-model="full_name"
            placeholder="نام و نام خانوادگی"
          />
        </div>

        <div class="form-group">
          <label>ایمیل</label>
          <input
            type="email"
            v-model="email"
            placeholder="example@gmail.com"
            :class="{ error: emailError, success: email && !emailError }"
          />
          <small class="error-text" v-if="emailError">
            {{ emailError }}
          </small>
        </div>

        <div class="form-group">
          <label>شماره موبایل</label>
          <input
            type="text"
            v-model="phone"
            placeholder="09123456789"
          />
        </div>

        <div class="form-group">
          <label>رمز عبور</label>
          <div class="password-box">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="حداقل ۸ کاراکتر"
              :class="{ error: passwordError, success: password && !passwordError }"
            />
            <button
              type="button"
              class="toggle"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? "🙈" : "👁" }}
            </button>
          </div>
          <small class="error-text" v-if="passwordError">
            {{ passwordError }}
          </small>
        </div>

        <div class="form-group">
          <label>تکرار رمز عبور</label>
          <div class="password-box">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="تکرار رمز عبور"
            />
            <button
              type="button"
              class="toggle"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              {{ showConfirmPassword ? "🙈" : "👁" }}
            </button>
          </div>
          <small class="error-text" v-if="confirmError">
            {{ confirmError }}
          </small>
        </div>

        <!-- ===== بخش جدید: انتخاب نقش ===== -->
        <div class="form-group role-group">
          <label>ثبت‌نام به عنوان</label>
          <div class="role-options">
            <label class="role-option">
              <input type="radio" value="user" v-model="role" />
              <span>کاربر عادی</span>
            </label>
            <label class="role-option">
              <input type="radio" value="admin" v-model="role" />
              <span>مدیر</span>
            </label>
          </div>
          <small class="hint">
            اگر مدیر سایت نیستید، گزینه «کاربر عادی» را انتخاب کنید.
          </small>
        </div>

        <button class="login-btn" :disabled="!isValid">
          ثبت نام
        </button>
      </form>

      <p class="register-link">
        قبلاً حساب دارید؟
        <RouterLink to="/login">ورود</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const full_name = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");
const confirmPassword = ref("");
const role = ref("user"); // مقدار پیش‌فرض: کاربر عادی

const showPassword = ref(false);
const showConfirmPassword = ref(false);

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

const confirmError = computed(() => {
  if (confirmPassword.value === "") return "";
  if (confirmPassword.value !== password.value)
    return "تکرار رمز عبور یکسان نیست.";
  return "";
});

const isValid = computed(() => {
  return (
    full_name.value.length > 2 &&
    phone.value.length >= 10 &&
    emailRegex.test(email.value) &&
    password.value.length >= 8 &&
    confirmPassword.value === password.value
  );
});

const register = async () => {
  try {
    await axios.post(
      "http://127.0.0.1:8000/users/api/register",
      {
        full_name: full_name.value,
        email: email.value,
        phone: phone.value,
        password: password.value,
        role: role.value, // ارسال نقش به بک‌اند
      }
    );

    alert("ثبت نام با موفقیت انجام شد.");
    router.push("/login");
  } catch (err: any) {
    alert(
      err.response?.data?.detail ??
      "خطا در ثبت نام"
    );
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  direction: rtl;
}

.login-card {
  width: 100%;
  max-width: 450px;
  background: white;
  padding: 35px;
  border-radius: 18px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
}

h1 {
  margin: 0;
  margin-bottom: 10px;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 22px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 13px;
  border: 1px solid #d5d5d5;
  border-radius: 10px;
  font-size: 15px;
  transition: 0.25s;
}

input:focus {
  outline: none;
  border-color: #2563eb;
}

.success {
  border-color: #22c55e;
}

.error {
  border-color: #ef4444;
}

.password-box {
  position: relative;
}

.toggle {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  cursor: pointer;
  font-size: 18px;
}

.hint {
  display: block;
  margin-top: 6px;
  color: #777;
  font-size: 12px;
}

.error-text {
  display: block;
  margin-top: 6px;
  color: #ef4444;
  font-size: 13px;
}

.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
  font-size: 14px;
}

.options a {
  text-decoration: none;
  color: #2563eb;
}

.remember {
  display: flex;
  gap: 8px;
  align-items: center;
}

.remember input {
  width: auto;
}

.login-btn {
  width: 100%;
  padding: 14px;
  border: none;
  background: #2563eb;
  color: white;
  font-size: 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.25s;
}

.login-btn:hover {
  background: #1d4ed8;
}

.login-btn:disabled {
  background: #bfc7d7;
  cursor: not-allowed;
}

.register-link {
  margin-top: 25px;
  text-align: center;
}

.register-link a {
  text-decoration: none;
  font-weight: bold;
  color: #2563eb;
}

/* ===== استایل‌های جدید برای انتخاب نقش ===== */
.role-group {
  margin-top: 6px;
}

.role-options {
  display: flex;
  gap: 24px;
  margin-top: 6px;
}

.role-option {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-weight: normal;
  font-size: 15px;
}

.role-option input[type="radio"] {
  width: 18px;
  height: 18px;
  accent-color: #2563eb;
  cursor: pointer;
  flex-shrink: 0;
}

.role-option span {
  user-select: none;
}
</style>