<script setup>
import { adminService } from "../../services";
import { ref, onMounted } from "vue";
import Chart from 'chart.js/auto';

const totalDoctors = ref(0)
const totalPatients = ref(0)
const totalAppointments = ref(0)
const pendingAppointments = ref(0)
const completedAppointments = ref(0)
const doctors = ref([])
const patients = ref([])
const appointments = ref([])
const pastAppointments = ref([])
const patientSearch = ref('')
const filteredPatients = ref([])
const doctorSearch = ref('')
const filteredDoctor = ref('')

let chartInstance = null

const loadDashboard = async () => {
  try {
    const response = await adminService.getDashboard()
    totalDoctors.value = response.data.total_doctors ?? 0
    totalPatients.value = response.data.total_patients ?? 0
    totalAppointments.value = response.data.total_appointments ?? 0
    pendingAppointments.value = response.data.pending_appointments_count ?? 0
    completedAppointments.value = response.data.completed_appointments_count ?? 0
    doctors.value = response.data.doctors ?? []
    patients.value = response.data.patients ?? []
    appointments.value = response.data.appointments ?? []
    pastAppointments.value = response.data.past_appointments ?? []
    filteredPatients.value = patients.value
    filteredDoctor.value = doctors.value
    
    setTimeout(() => renderChart(), 100)
  } catch (e) {
    console.error('Failed to load dashboard data:', e)
  }
}

const renderChart = () => {
  const ctx = document.getElementById('appointmentChart')
  if (!ctx) return
  
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Pending', 'Completed', 'Cancelled'],
      datasets: [{
        data: [pendingAppointments.value, completedAppointments.value, totalAppointments.value - pendingAppointments.value - completedAppointments.value],
        backgroundColor: ['#198754', '#0dcaf0', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

const blockUser = async (userId) => {
  try {
    const response = await adminService.blockUser(userId)
    alert(response.data.msg)
    await loadDashboard()
  } catch (e) {
    alert(e.response?.data?.msg || 'Failed to update user status')
  }
}

const deleteUser = async (userId) => {
  try {
    const response = await adminService.deleteUser(userId)
    alert(response.data.msg)
    await loadDashboard()
  } catch (e) {
    alert(e.response?.data?.msg || 'Failed to delete user')
  }
}

const searchPatient = () => {
  const query = patientSearch.value.toLowerCase().trim()
  if (!query) {
    filteredPatients.value = patients.value
  } else {
    filteredPatients.value = patients.value.filter(p =>
      p.name.toLowerCase().includes(query) ||
      p.email.toLowerCase().includes(query)
    )
  }
}

const searchDoctor = () => {
  const query = doctorSearch.value.toLowerCase().trim()
  if (!query) {
    filteredDoctor.value = doctors.value
  } else {
    filteredDoctor.value = doctors.value.filter(d =>
      d.name.toLowerCase().includes(query) ||
      d.dept.toLowerCase().includes(query)
    )
  }
}

const timeLabel = (slot) => slot === 'morning' ? '9AM-1PM' : '3PM-7PM'

onMounted(loadDashboard)
</script>

<template>
<div class="container-fluid">
    <div class="row">
        <main class="col-12 px-md-4">
            <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <div class="btn-toolbar mb-2 mb-md-0">
                    <router-link to="/admin/add-doctor" class="btn btn-primary">
                        <i class="bi bi-person-plus me-1"></i> Add Doctor
                    </router-link>
                    <router-link to="/admin/add-dept" class="btn btn-primary ms-2">
                        <i class="bi bi-person-plus"></i> Add Department
                    </router-link>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Total Doctors</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ totalDoctors }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-person-badge fs-1 text-primary"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Patients</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ totalPatients }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-people fs-1 text-success"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Appointments</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ totalAppointments }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-calendar-check fs-1 text-info"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-lg-6 col-md-6 col-sm-6 col-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Pending</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ pendingAppointments }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-clock fs-1 text-warning"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-pie-chart me-2"></i>Appointment Status</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="appointmentChart" height="100"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-6 col-md-12 mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center flex-wrap">
                            <h5 class="mb-0 mb-sm-2"><i class="bi bi-people me-2"></i>Doctors List</h5>
                            <form class="d-flex flex-grow-1 flex-sm-grow-0 ms-2" style="max-width: 300px;">
                                <input class="form-control form-control-sm me-2" v-model="doctorSearch" @input="searchDoctor"
                                       type="text" placeholder="Search by name/department...">
                            </form>
                        </div>
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead class="table-light">
                                        <tr>
                                            <th>Name</th>
                                            <th>Specialization</th>
                                            <th>Experience</th>
                                            <th>Status</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="doctor in filteredDoctor" :key="doctor.id">
                                            <td>{{ doctor.name }}</td>
                                            <td>{{ doctor.dept }}</td>
                                            <td>{{ doctor.experience }} years</td>
                                            <td>
                                                <span class="badge" :class="doctor.role.startsWith('BLOCKED') ? 'bg-danger' : 'bg-success'">
                                                    {{ doctor.role.startsWith('BLOCKED') ? 'Blocked' : 'Active' }}
                                                </span>
                                            </td>
                                            <td>
                                                <div class="btn-group" role="group">
                                                    <a :href="'/profile/' + doctor.id">
                                                        <button type="button" class="btn btn-sm btn-outline-success" title="Edit">
                                                            <i class="bi bi-pen"></i>
                                                        </button>
                                                    </a>
                                                    <button type="button" class="btn btn-sm btn-outline-warning" :title="doctor.role.startsWith('BLOCKED') ? 'Unblock' : 'Block'" @click="blockUser(doctor.id)">
                                                        <i :class="doctor.role.startsWith('BLOCKED') ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                                                    </button>
                                                    <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="deleteUser(doctor.id)">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr v-if="filteredDoctor.length === 0">
                                            <td colspan="5" class="text-center text-muted py-4">No doctors found</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-6 col-md-12 mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center flex-wrap">
                            <h5 class="mb-0"><i class="bi bi-person-lines-fill me-2"></i>Registered Patients</h5>
                            <input class="form-control form-control-sm" v-model="patientSearch" @input="searchPatient"
                                   type="text" placeholder="Search by name/email...">
                        </div>
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead class="table-light">
                                        <tr>
                                            <th>Patient</th>
                                            <th>Age</th>
                                            <th>Email</th>
                                            <th>Status</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="patient in filteredPatients" :key="patient.id">
                                            <td>{{ patient.name }}</td>
                                            <td>{{ patient.age }}</td>
                                            <td>{{ patient.email }}</td>
                                            <td>
                                                <span class="badge" :class="patient.role.startsWith('BLOCKED') ? 'bg-danger' : 'bg-success'">
                                                    {{ patient.role.startsWith('BLOCKED') ? 'Blocked' : 'Active' }}
                                                </span>
                                            </td>
                                            <td>
                                                <div class="btn-group" role="group">
                                                    <a :href="'/profile/' + patient.id">
                                                        <button type="button" class="btn btn-sm btn-outline-success" title="Edit">
                                                            <i class="bi bi-pen"></i>
                                                        </button>
                                                    </a>
                                                    <button type="button" class="btn btn-sm btn-outline-warning" :title="patient.role.startsWith('BLOCKED') ? 'Unblock' : 'Block'" @click="blockUser(patient.id)">
                                                        <i :class="patient.role.startsWith('BLOCKED') ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                                                    </button>
                                                    <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="deleteUser(patient.id)">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr v-if="filteredPatients.length === 0">
                                            <td colspan="5" class="text-center text-muted py-4">No patients found</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12 mb-4">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-calendar-check me-2"></i>Upcoming Appointments</h5>
                        </div>
                        <div class="card-body p-0">
                            <div class="list-group list-group-flush">
                                <div v-if="!appointments.length" class="list-group-item text-center py-4">
                                    <p class="text-muted mb-0">No upcoming appointments</p>
                                </div>
                                <div class="list-group-item" v-for="apt in appointments" :key="apt.id">
                                    <div class="d-flex w-100 justify-content-between flex-wrap">
                                        <div class="mb-2 mb-sm-0">
                                            <h6 class="mb-1">{{ apt.patient_name }}</h6>
                                            <p class="mb-1">{{ apt.doctor_name }}, {{ apt.department }}</p>
                                            <small class="text-muted">
                                                <i class="bi bi-calendar me-1"></i> {{ apt.date }},
                                                {{ timeLabel(apt.time_slot) }}
                                            </small>
                                        </div>
                                        <div>
                                            <a :href="`/patient-history/${apt.patient_id}`" class="btn btn-sm btn-outline-primary">
                                                <i class="bi bi-person-lines-fill"></i> History
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12 mb-4">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0"><i class="bi bi-calendar-check me-2"></i>Past Appointments</h5>
                        </div>
                        <div class="card-body p-0">
                            <div class="list-group list-group-flush">
                                <div v-if="!pastAppointments.length" class="list-group-item text-center py-4">
                                    <p class="text-muted mb-0">No past appointments</p>
                                </div>
                                <div class="list-group-item" v-for="apt in pastAppointments" :key="apt.id">
                                    <div class="d-flex w-100 justify-content-between flex-wrap">
                                        <div class="mb-2 mb-sm-0">
                                            <h6 class="mb-1">{{ apt.patient_name }}</h6>
                                            <p class="mb-1">{{ apt.doctor_name }}, {{ apt.department }}</p>
                                            <small class="text-muted">
                                                <i class="bi bi-calendar me-1"></i> {{ apt.date }},
                                                {{ timeLabel(apt.time_slot) }}
                                            </small>
                                        </div>
                                        <div>
                                            <a :href="`/patient-history/${apt.patient_id}`" class="btn btn-sm btn-outline-primary">
                                                <i class="bi bi-person-lines-fill"></i> History
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>

</template>

<style scoped>

</style>
