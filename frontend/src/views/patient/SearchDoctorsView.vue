<script setup>
import { ref, onMounted } from 'vue'
import { patientService } from '../../services'

const departments = ref([])
const doctors = ref([])
const searchName = ref('')
const searchDept = ref('')
const searchDate = ref('')
const searchTime = ref('')
const dates = ref([])

const loadDepts = async () => {
  const res = await patientService.getDepartments()
  departments.value = res.data
}

const loadDates = () => {
  const today = new Date()
  for (let i = 0; i < 7; i++) {
    const d = new Date(today)
    d.setDate(today.getDate() + i)
    dates.value.push(d.toISOString().split('T')[0])
  }
}

const searchByName = async () => {
  const res = await patientService.searchDoctors(searchName.value, searchDept.value || '')
  doctors.value = res.data
}

const searchByAvailability = async () => {
  if (!searchDept.value) return
  const res = await patientService.searchDoctors('', searchDept.value)
  doctors.value = res.data
}

const clearFilters = () => {
  searchName.value = ''
  searchDept.value = ''
  searchDate.value = ''
  searchTime.value = ''
  doctors.value = []
}

onMounted(() => {
  loadDepts()
  loadDates()
})
</script>

<template>
<div class="container py-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Search Doctors</h2>
  </div>

  <div class="card mb-4 shadow-sm">
    <div class="card-header bg-light">
      <h5>Search by Doctor Name</h5>
    </div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-12">
          <label for="doctor_name" class="form-label">Enter doctor's name</label>
          <input
            type="text"
            class="form-control"
            id="doctor_name"
            v-model="searchName"
            placeholder="Type name and click Search">
        </div>
        <div class="col-12">
          <button @click="searchByName" class="btn btn-success">Search by Name</button>
        </div>
      </div>
    </div>
  </div>

  <div class="card mb-4 shadow-sm">
    <div class="card-header bg-light">
      <h5>Search by Availability</h5>
    </div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-md-4">
          <label for="department" class="form-label">Department</label>
          <select class="form-select" id="department" v-model="searchDept">
            <option value="">All Departments</option>
            <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
          </select>
        </div>

        <div class="col-md-4">
          <label for="date" class="form-label">Date</label>
          <select class="form-select" id="date" v-model="searchDate">
            <option value="">Select Date</option>
            <option v-for="d in dates" :key="d" :value="d">{{ d }}</option>
          </select>
        </div>

        <div class="col-md-4">
          <label for="time_slot" class="form-label">Time Slot</label>
          <select class="form-select" id="time_slot" v-model="searchTime">
            <option value="">Time</option>
            <option value="morning">9 AM – 1 PM</option>
            <option value="evening">3 PM – 7 PM</option>
          </select>
        </div>

        <div class="col-12">
          <button @click="searchByAvailability" class="btn btn-primary">Search by Availability</button>
          <button @click="clearFilters" class="btn btn-outline-secondary ms-2">
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="doctors.length">
    <h5>Available Results</h5>
    <div class="row row-cols-1 row-cols-md-2 g-4">
      <div class="col" v-for="doctor in doctors" :key="doctor.id">
        <div class="card h-100 shadow-sm">
          <div class="card-header bg-primary text-white">
            <h5>{{ doctor.name }}</h5>
          </div>
          <div class="card-body">
            <p class="card-text">
              <strong>Department:</strong> {{ doctor.dept }}<br>
              <strong>Experience:</strong> {{ doctor.experience }}<br>
              <strong>Email:</strong> {{ doctor.email }}<br>
            </p>
          </div>
          <div class="card-footer bg-light text-center">
            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
              <a v-if="doctor.id" :href="`/doctor/${doctor.id}`" class="btn btn-outline-info btn-sm px-3">
                View Details
              </a>
              <router-link v-if="doctor.id" :to="`/patient/book-slot/${doctor.id}`" class="btn btn-primary btn-sm px-3">
                Book Slot
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="searchName || searchDept" class="alert alert-warning">
    No doctors available.
  </div>
</div>

</template>