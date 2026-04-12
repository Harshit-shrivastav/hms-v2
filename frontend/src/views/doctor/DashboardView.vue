<script setup>
import { ref, onMounted } from 'vue'
import { doctorService } from '../../services'
import Chart from 'chart.js/auto'

const today = ref(0)
const pending = ref(0)
const completed = ref(0)
const cancelled = ref(0)
const assigned = ref(0)
const appointments = ref([])
const patients = ref([])

const load = async () => {
  const res = await doctorService.getDashboard()
  today.value = res.data.today_count
  pending.value = res.data.pending_count
  completed.value = res.data.completed_count
  cancelled.value = res.data.cancelled_count
  assigned.value = res.data.assigned_count
  appointments.value = res.data.appointments
  patients.value = res.data.patients
  
  setTimeout(() => renderChart(), 100)
}

const cancel = async (id) => {
  await doctorService.cancelAppointment(id)
  appointments.value = appointments.value.filter(a => a.id !== id)
  load()
}

const complete = async (id) => {
  await doctorService.completeAppointment(id)
  appointments.value = appointments.value.filter(a => a.id !== id)
  load()
}

const timeLabel = (slot) => slot === 'morning' ? '9AM-1PM' : '3PM-7PM'

let chartInstance = null

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
        data: [pending.value, completed.value, cancelled.value],
        backgroundColor: ['#198754', '#0dcaf0', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

onMounted(load)
</script>

<template>
<div class="container-fluid">
    <div class="row">
        <main class="col-md-12 px-md-4">
            <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <div class="btn-toolbar mb-2 mb-md-0">
                    <a href="/doctor/slots" class="btn btn-primary">
                        <i class="bi bi-clock me-1"></i> Provide Availability
                    </a>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Today's Appointments</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ today }}</div>
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
                                    <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Pending</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ pending }}</div>
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
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ completed }}</div>
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
                                    <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">Cancelled</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ cancelled }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-x-circle fs-1 text-danger"></i>
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
                                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Assigned Patients</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">{{ assigned }}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="bi bi-people fs-1 text-warning"></i>
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

            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-calendar-check me-2"></i>Upcoming Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Sr No</th>
                                    <th>Patient Name</th>
                                    <th>Slot</th>
                                    <th>Patient History</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(apt, i) in appointments" :key="apt.id">
                                    <td>{{ i + 1 }}</td>
                                    <td>{{ apt.patient_name }}</td>
                                    <td>{{ apt.date }} - {{ timeLabel(apt.time_slot) }}</td>
                                    <td>
                                        <a :href="`/doctor/update-history/${apt.id}`">
                                            <button class="btn btn-sm btn-outline-warning me-1">Update</button>
                                        </a>
                                    </td>
                                    <td>
                                        <button class="btn btn-sm btn-outline-danger me-1" @click="cancel(apt.id)">Cancel</button>
                                        <button class="btn btn-sm btn-outline-success" @click="complete(apt.id)">Mark as Done</button>
                                    </td>
                                </tr>
                                <tr v-if="!appointments.length">
                                    <td colspan="5" class="text-center py-4">No upcoming appointments</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-people me-2"></i>Assigned Patients</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Visit No</th>
                                    <th>Patient Name</th>
                                    <th>Age</th>
                                    <th>Contact</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(p, i) in patients" :key="p.id">
                                    <td>{{ i + 1 }}</td>
                                    <td>{{ p.name }}</td>
                                    <td>{{ p.age }}</td>
                                    <td>{{ p.email }}</td>
                                    <td>
                                        <a :href="`/doctor/patient-history/${p.id}`">
                                            <button class="btn btn-sm btn-outline-primary">View</button>
                                        </a>
                                    </td>
                                </tr>
                                <tr v-if="!patients.length">
                                    <td colspan="5" class="text-center py-4">No assigned patients</td>
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
