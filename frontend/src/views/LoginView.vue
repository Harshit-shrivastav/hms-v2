<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const status = ref(false)

const redirectByRole = (role) => {
  if (role === 'admin') {
    router.push('/admin')
  } else if (role === 'doctor') {
    router.push('/doctor')
  } else if (role === 'patient') {
    router.push('/patient')
  } else {
    router.push('/dashboard')
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await authService.login(email.value, password.value)
    console.log('Login successful:', response.data)

    alert('Login successful!')

    const role = response.data.user.role
    redirectByRole(role)
  } catch (err) {
    error.value = err.response?.data?.msg || 'Login failed. Please try again.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const response = await authService.isLoggedIn()
    if (response.data.logged_in) {
      const profileResponse = await authService.getProfile()
      const role = profileResponse.data.role
      redirectByRole(role)
    }
  } catch (err) {
    console.log('Not logged in:', err)
  }
})
</script>

<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100">
    <div class="card p-5 shadow" style="width: 400px;">
      <h2 class="text-center mb-4">User Login</h2>

      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="InputEmail" class="form-label">Email address</label>
          <input 
            type="email" 
            class="form-control" 
            id="InputEmail" 
            v-model="email"
            aria-describedby="emailHelp" 
            name="email" 
            required
            :disabled="loading"
          >
        </div>

        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input 
            type="password" 
            class="form-control" 
            id="InputPassword" 
            v-model="password"
            name="password" 
            required
            :disabled="loading"
          >
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          Login
        </button>
      </form>

      <div class="mt-3 text-center">
        <p class="mb-0">Not yet Registered?
          <router-link to="/patient/register" class="text-decoration-none">Register Now</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
