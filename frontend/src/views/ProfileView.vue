<script setup>
import { ref, onMounted } from 'vue'
import { patientService, adminService } from '../services'
import { useRoute } from 'vue-router'

const userId = useRoute().params.id
const userRole = ref('')

const name = ref('')
const email = ref('')
const gender = ref('')
const age = ref('')
const experience = ref('')
const department = ref('')
const error = ref('')
const success = ref('')

onMounted(async () => {
  try {
    const api = userId ? adminService.getUser : patientService.getProfile
    const response = await api(userId)
    name.value = response.data.name || ''
    email.value = response.data.email || ''
    gender.value = response.data.gender || ''
    age.value = response.data.age || ''
    experience.value = response.data.experience || ''
    department.value = response.data.dept || ''
    userRole.value = response.data.role || ''
  } catch (e) {
    error.value = 'Failed to load profile data'
  }
})

const updateProfile = async () => {
  error.value = ''
  success.value = ''

  try {
    const api = userId ? adminService.updateUser : patientService.updateProfile
    const data = { name: name.value, email: email.value, gender: gender.value, age: age.value, experience: experience.value, dept: department.value }
    await api(userId, data)
    success.value = 'Profile updated successfully!'
    setTimeout(() => success.value = '', 3000)
  } catch (e) {
    error.value = e.response?.data?.msg || 'Failed to update profile'
  }
}
</script>

<template>
<div class="container mt-5">
  <div class="row">
    <div class="col-md-8 mx-auto">
      <h2>{{ userId ? 'Edit User Profile' : 'Update Profile' }}</h2>

      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="name" name="name" v-model="name" required>
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" name="email" v-model="email" required>
        </div>

        <div class="mb-3" v-if="userRole !== 'doctor' && userRole !== 'BLOCKED_doctor'">
          <label for="gender" class="form-label">Gender</label>
          <select class="form-control" id="gender" name="gender" v-model="gender">
            <option value="" disabled>Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="mb-3" v-if="userRole !== 'doctor' && userRole !== 'BLOCKED_doctor'">
          <label for="age" class="form-label">Age</label>
          <input type="number" class="form-control" id="age" name="age" v-model="age" min="1" max="120" required>
        </div>

        <div class="mb-3" v-if="userRole === 'doctor' || userRole === 'BLOCKED_doctor'">
          <label for="experience" class="form-label">Experience (Years)</label>
          <input type="number" class="form-control" id="experience" name="experience" v-model="experience" min="0" max="50">
        </div>

        <div class="mb-3" v-if="userRole === 'doctor' || userRole === 'BLOCKED_doctor'">
          <label for="department" class="form-label">Department/Specialisation</label>
          <input type="text" class="form-control" id="department" name="department" v-model="department" placeholder="e.g., Cardiology, Neurology">
        </div>

        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-if="success" class="alert alert-success" role="alert">
          {{ success }}
        </div>

        <button type="submit" class="btn btn-primary">
          Update Profile
        </button>
      </form>

      <hr class="my-4">
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
