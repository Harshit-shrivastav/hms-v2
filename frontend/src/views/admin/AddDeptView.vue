<script setup>
import { adminService } from "../../services";
import { ref, onMounted } from "vue";

const departmentName = ref('')
const departments = ref([])
const loading = ref(false)

const loadDepartments = async () => {
  const response = await adminService.getDepartments()
  departments.value = response.data.departments || []
}

const addDepartment = async () => {
  loading.value = true
  await adminService.createDepartment({ name: departmentName.value })
  departmentName.value = ''
  loadDepartments()
  loading.value = false
}

onMounted(() => {
  loadDepartments()
})
</script>

<template>
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-12 col-md-8 col-lg-6">
      <h2 class="text-center mb-4">Department Management</h2>

      <div class="card mb-4">
        <div class="card-body text-center">
          <h5 class="card-title mb-3">Add New Department</h5>
          <form @submit.prevent="addDepartment" class="d-flex flex-column align-items-center">
            <div class="w-100" style="max-width: 400px;">
              <div class="input-group">
                <input type="text"
                       class="form-control"
                       placeholder="Enter department name"
                       v-model="departmentName"
                       required>
                <button class="btn btn-primary" type="submit" :disabled="loading">
                  {{'Add Department'}}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-body text-center">
          <h5 class="card-title mb-3">Available Departments</h5>
          <div class="w-100" style="max-width: 400px; margin: 0 auto;">
            <select class="form-select" id="departmentDropdown" v-if="departments.length > 0">
              <option value="" disabled selected>Select a department</option>
              <option v-for="dept in departments" :key="dept.id || dept.name" :value="dept.name">
                {{ dept.name }}
              </option>
            </select>
            <p v-else class="text-muted">No departments available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
