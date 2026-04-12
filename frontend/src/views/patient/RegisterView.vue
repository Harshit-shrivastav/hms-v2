<script setup>
import {ref, onMounted} from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../../services'

const router = useRouter()
const name = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const gender = ref('')
const age = ref('')
const error = ref('')
const loading = ref(false)

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
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await authService.register(name.value, email.value, username.value, password.value, gender.value, age.value)
    alert('Registration successful!')
    router.push('/patient')
  }
  catch (e) {
    console.log(e)
    error.value = e.response?.data?.msg || 'Registration failed'
  }
  finally {
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
<div id="" class="align-items-center justify-content-center mt-5"></div>
<div class="container card shadow" style="width:500px; height: auto;">
  <h2>Create an Account</h2>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="InputName" class="form-label">Full Name</label>
      <input type="text" class="form-control" id="InputName" name="name" required v-model="name">
    </div>
    <div class="mb-3">
      <label for="InputName" class="form-label">User Name</label>
      <input type="text" class="form-control" id="InputUsername" name="username" required v-model="username">
    </div>
<div class="mb-3">
  <label for="InputGender" class="form-label">Gender</label>
  <select class="form-select" id="InputGender" name="gender" required v-model="gender">
    <option value="" disabled selected>Select gender</option>
    <option value="Male">Male</option>
    <option value="Female">Female</option>
    <option value="Other">Other</option>
  </select>
</div>
<div class="mb-3">
  <label for="InputAge" class="form-label">Age</label>
  <input type="number"
         class="form-control"
         id="InputAge"
         name="age"
         min="0"
         max="150"
         maxlength="3"
         v-model="age"
         required>
</div>
    <div class="mb-3">
      <label for="InputEmail" class="form-label">Email address</label>
      <input type="email" class="form-control" id="InputEmail" aria-describedby="emailHelp" name="email" v-model="email" required>
      <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
    </div>
    <div class="mb-3">
      <label for="InputPassword" class="form-label">Password</label>
      <input type="password" class="form-control" id="InputPassword" name="password" required v-model="password">
    </div>
    <div class="mb-3">
      <label for="InputConfirmPassword" class="form-label">Confirm Password</label>
      <input type="password" class="form-control" id="InputConfirmPassword" name="confirm_password" required v-model="confirmPassword">
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>`
    <button type="submit" class="btn btn-primary" :disabled="loading">Register</button>
  </form>

  <div class="mt-3">
    <p>Already have an account? <router-link to="/login"> Login here</router-link></p>
  </div>
</div>

</template>

<style scoped>

</style>