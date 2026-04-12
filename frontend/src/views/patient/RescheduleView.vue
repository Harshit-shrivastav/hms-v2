<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { patientService } from '../../services'

const route = useRoute()
const router = useRouter()
const aptId = ref(route.query.id)
const apt = ref(null)
const dates = ref([])
const form = ref({ date: '', slot: '' })
const msg = ref('')
const msgType = ref('')
const loading = ref(false)

const load = async () => {
  try {
    const res = await patientService.getAppointments()
    const aptData = res.data.data.find(a => a.id == aptId.value)
    if (aptData) {
      apt.value = aptData
    }
    
    const today = new Date()
    for (let i = 1; i <= 7; i++) {
      const d = new Date(today)
      d.setDate(today.getDate() + i)
      dates.value.push(d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }))
    }
  } catch (e) {
    msg.value = 'Failed to load appointment'
    msgType.value = 'danger'
  }
}

const submit = async () => {
  loading.value = true
  try {
    await patientService.rescheduleAppointment(aptId.value, {
      date: form.value.date,
      time_slot: form.value.slot
    })
    msg.value = 'Appointment rescheduled!'
    msgType.value = 'success'
    setTimeout(() => router.push('/patient'), 1500)
  } catch (e) {
    msg.value = e.response?.data?.msg || 'Failed to reschedule'
    msgType.value = 'danger'
  }
  loading.value = false
}

const timeLabel = (slot) => slot === 'morning' ? '9AM-1PM' : '3PM-7PM'

onMounted(load)
</script>

<template>
<div class="container py-4">
    <div class="card shadow-sm">
      <div class="card-header bg-white">
        <h5 class="card-title mb-0">Reschedule Appointment #{{ aptId }}</h5>
      </div>
      <div class="card-body">
        <div v-if="msg" :class="`alert alert-${msgType}`">{{ msg }}</div>
        
        <div v-if="apt" class="alert alert-info mb-4">
          <strong>Current:</strong> {{ apt.date }} - {{ timeLabel(apt.time_slot) }} with {{ apt.doc_name }}
        </div>

        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="date" class="form-label fw-bold">Date</label>
            <select name="date" id="date" v-model="form.date" class="form-select" required>
              <option v-for="d in dates" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>

          <div class="mb-4">
            <label for="slot" class="form-label fw-bold">Slot</label>
            <select name="slot" id="slot" v-model="form.slot" class="form-select" required>
              <option value="morning">9:00 AM - 1:00 PM</option>
              <option value="evening">3:00 PM - 7:00 PM</option>
            </select>
          </div>

          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-success flex-grow-1" :disabled="loading">
              Reschedule
            </button>
            <a href="/patient" class="btn btn-outline-secondary flex-grow-1">
              Cancel
            </a>
          </div>
        </form>
      </div>
    </div>
  </div>

</template>
