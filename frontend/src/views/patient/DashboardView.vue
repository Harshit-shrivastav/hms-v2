<script setup>
import { ref, onMounted } from 'vue'
import { patientService } from '../../services'

const departments = ref([])
const dashboardData = ref(null)
const upcomingAppointments = ref([])
const error = ref('')
const exportMessage = ref('')

const loadDashboard = async() =>{
  try {
    const res = await patientService.getPatientDashboard()
    dashboardData.value = res.data.data
  } catch (e) {
    error.value = 'Failed to load dashboard'
  }
}

const loadDepts = async () => {
  try {
    const res = await patientService.getDepartments()
    departments.value = res.data
  } catch (e) {
    error.value = 'Failed to load departments'
  }
}

const loadAppointments = async () => {
  try {
    const res = await patientService.getAppointments()
    upcomingAppointments.value = res.data.data.filter(apt => apt.status === 'booked')
  } catch (e) {
    error.value = 'Failed to load appointments'
  }
}

const cancelAppointment = async (id) => {
  await patientService.cancelAppointment(id)
  loadAppointments()
  loadDashboard()
}

const exportToCsv = async () => {
  try {
    exportMessage.value = 'Sending export request...'
    const res = await patientService.exportPatientData()
    exportMessage.value = 'Export email sent successfully! Check your inbox.'
    setTimeout(() => { exportMessage.value = '' }, 5000)
  } catch (e) {
    exportMessage.value = 'Failed to send export request. Please try again.'
    setTimeout(() => { exportMessage.value = '' }, 5000)
  }
}

const timeLabel = (slot) => slot === 'morning' ? '9AM-1PM' : '3PM-7PM'

onMounted(() => {
  loadDashboard()
  loadDepts()
  loadAppointments()
})
</script>

<template>
<div class="container-fluid mt-5">
    <div class="row">
        <main class="col-md-12 px-md-4">
            <button class="btn btn-primary mb-2" @click="exportToCsv" :disabled="exportMessage !== ''">
                {{ exportMessage || 'Export CSV' }}
            </button>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div class="row mb-4" v-if="!error">
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Total Appointments</div>
                                    <b>{{ dashboardData?.total_appointments || 0 }}</b>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-calendar-check fs-1 text-primary"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Upcoming</div>
                                    <b>{{ dashboardData?.upcoming_appointments || 0 }}</b>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-clock fs-1 text-success"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">Cancelled</div>
                                    <b>{{ dashboardData?.cancelled_appointments || 0 }}</b>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-clock fs-1 text-success"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Completed</div>
                                    <b>{{ dashboardData?.completed_appointments || 0 }}</b>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-check-circle fs-1 text-info"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Departments</div>
                                    <b>{{ departments.length }}</b>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-building fs-1 text-warning"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


            </div>

            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-building me-2"></i>Departments</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Department Name</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="dept in departments" :key="dept.id">
                                    <td>{{ dept.name }}</td>
                                    <td>
                                        <router-link :to="`/patient/departments/${dept.id}`" class="btn btn-sm btn-outline-primary">
                                            View Doctors
                                        </router-link>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-calendar-check me-2"></i>Upcoming Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Sr. No.</th>
                                    <th>Appointment Date</th>
                                    <th>Doctor</th>
                                    <th>Department</th>
                                    <th>Time</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(apt, i) in upcomingAppointments" :key="apt.id">
                                    <td>{{ i + 1 }}</td>
                                    <td>{{ apt.date }}</td>
                                    <td>{{ apt.doc_name }}</td>
                                    <td>{{ apt.doc_dept }}</td>
                                    <td>{{ timeLabel(apt.time_slot) }}</td>
                                    <td>
                                        <a :href="`/patient/reschedule?id=${apt.id}`" class="btn btn-sm btn-outline-warning me-1">
                                            <i class="bi bi-calendar-event"></i> Reschedule
                                        </a>
                                        <button class="btn btn-sm btn-outline-danger" @click="cancelAppointment(apt.id)">Cancel</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>

</template>

<style scoped>
</style>
