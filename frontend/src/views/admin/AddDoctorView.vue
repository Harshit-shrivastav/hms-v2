<script setup>
import { doctorService, adminService } from "../../services";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter()

const fullName = ref('')
const department = ref('')
const experience = ref('')
const email = ref('')
const mobile = ref('')
const username = ref('')
const password = ref('')
const departments = ref([])
const loading = ref(false)

onMounted(async () => {
  const response = await adminService.getDepartments()
  departments.value = response.data.departments || []
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await doctorService.create({
      full_name: fullName.value,
      department: department.value,
      experience: experience.value,
      email: email.value,
      mobile: mobile.value,
      username: username.value,
      password: password.value
    })
    alert('Doctor added successfully!')
    router.push('/admin')
  } catch (e) {
    alert(e.response?.data?.msg || 'Failed to add doctor')
  } finally {
    loading.value = false
  }
}
</script>

<template>
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h3 class="text-center">Add Doctor</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="full_name" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="full_name" v-model="fullName" required>
              </div>
              <div class="col-md-6 mb-3">
                <label for="department" class="form-label">Department/Specialisation</label>
                <select class="form-select" id="department" v-model="department" required>
                  <option value="">Select Department</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.name">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="experience" class="form-label">Experience (Years)</label>
                <input type="number" class="form-control" id="experience" v-model="experience" min="0" required>
              </div>
              <div class="col-md-4 mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
              </div>
              <div class="col-md-4 mb-3">
                <label for="mobile" class="form-label">Mobile Number</label>
                <input type="tel" class="form-control" id="mobile" v-model="mobile" required>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" v-model="username" required>
              </div>
              <div class="col-md-6 mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
            </div>

            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ 'Add doctor' }}
              </button>
              <a href="/admin/dashboard" class="btn btn-secondary">Cancel</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
