<script setup lang="ts">
import axios from "axios"
import { useRouter } from "vue-router"
import { ref, computed } from "vue"
import { useToast } from "vue-toastification"

const router = useRouter()
const toast = useToast()

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

    toast.success("ورود با موفقیت انجام شد.", {
      timeout: 3000,
    })

    router.push("/")

  }

  catch (err: any) {

    toast.error(
      err.response?.data?.detail ?? "خطا در ورود",
      {
        timeout: 3000,
      }
    )

  }

}
</script>