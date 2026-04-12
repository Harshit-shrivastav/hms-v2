<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold">HMS</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/login" class="btn btn-danger ms-2">Login</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/patient/register" class="btn btn-primary ms-2">Sign Up</router-link>
          </li>
          <li class="nav-item dropdown" v-if="isLoggedIn">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              <i class="bi bi-person-fill"></i>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="userRole === 'patient'"><router-link to="/patient/search-doctors" class="dropdown-item">Search Doctors</router-link></li>
              <li v-if="userRole === 'patient'"><router-link to="/my-history" class="dropdown-item">My History</router-link></li>
              <li v-if="userRole !== 'doctor'"><router-link to="/profile" class="dropdown-item">Profile</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a href="#" class="dropdown-item" @click.prevent="handleLogout">Logout</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../../services'

const router = useRouter()
const isLoggedIn = ref(false)
const userRole = ref('')

const checkAuth = async () => {
  try {
    const response = await authService.isLoggedIn()
    isLoggedIn.value = response.data.logged_in
    userRole.value = response.data.user?.role || ''
  } catch (e) {
    isLoggedIn.value = false
    userRole.value = ''
  }
}

onMounted(() => {
  checkAuth()
})

router.afterEach(() => {
  checkAuth()
})

const handleLogout = async () => {
  try {
    await authService.logout()
    isLoggedIn.value = false
    userRole.value = ''
    alert('Logged out successfully')
    router.push('/login')
  }
  catch (e) {
    alert(e)
    console.error('logout error', e)
  }
}
</script>

<style scoped>
.btn-primary {
  background-color: #ffc107;
  border: none;
  color: #000;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #ffb300;
}
</style>
