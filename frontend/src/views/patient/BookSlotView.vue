<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { patientService } from '../../services'

const route = useRoute()
const router = useRouter()
const dates = ref([])
const availability = ref({})
const selected = ref(null)
const loading = ref(false)
const msg = ref('')
const msgType = ref('')
const showPayment = ref(false)

const load = async () => {
  loading.value = true
  const res = await patientService.getDoctorSlots(route.params.doctorId)
  dates.value = res.data.dates
  availability.value = res.data.availability
  loading.value = false
}

const isAvail = (d, s) => availability.value[d][s]
const select = (date, time_slot) => selected.value = { date, time_slot }

const book = async () => {
  if (!selected.value) return
  showPayment.value = true
}

const confirmPayment = async () => {
  loading.value = true
  showPayment.value = false
  try {
    await patientService.bookAppointment(route.params.doctorId, selected.value.date, selected.value.time_slot)
    msg.value = 'Appointment booked successfully!'
    msgType.value = 'success'
    setTimeout(() => router.push('/patient'), 1500)
  } catch (e) {
    msg.value = e.response?.data?.msg || 'Booking failed'
    msgType.value = 'danger'
  }
  loading.value = false
}

const SLOTS = [
  { key: 'morning', label: '9AM-1PM' },
  { key: 'evening', label: '3PM-7PM' }
]

onMounted(load)
</script>

<template>
<div class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <h1 class="text-center mb-4 text-primary">Doctor's Availability</h1>

                <div v-if="msg" :class="`alert alert-${msgType}`">{{ msg }}</div>

                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <table class="table table-borderless">
                            <thead>
                                <tr>
                                    <th class="text-center">Date</th>
                                    <th class="text-center">Morning</th>
                                    <th class="text-center">Evening</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="date in dates" :key="date">
                                    <td class="text-center fw-bold">{{ date }}</td>
                                    <td v-for="{ key, label } in SLOTS" :key="key">
                                        <div class="border p-3 rounded text-center cursor-pointer"
                                            :class="isAvail(date, key) ? 'bg-success bg-opacity-10 border-success' : 'bg-danger bg-opacity-10 border-danger'"
                                            @click="isAvail(date, key) && select(date, key)"
                                        >
                                            <input type="radio" name="slots" :checked="selected?.date === date && selected?.time_slot === key"
                                                :disabled="!isAvail(date, key)" class="me-2 pointer-events-none">
                                            <span :class="isAvail(date, key) ? 'text-success' : 'text-danger'">{{ label }}</span>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="text-center mt-4">
                            <button class="btn btn-primary px-5 py-2" @click="book" :disabled="loading || !selected">
                                Book Selected Slot
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showPayment" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">Payment</h5>
                </div>
                <div class="modal-body">
                    <p class="mb-3"><strong>Appointment Fee:</strong> ₹500</p>
                    
                    <div class="alert alert-info">
                        <p class="mb-1"><strong>UPI ID:</strong> hms@hospital</p>
                        <p class="mb-0 small text-muted">pay to above UPI ID </p>
                    </div>
                    
                    <p class="text-muted small">Click "Confirm Payment" after completing UPI payment</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="showPayment = false">Cancel</button>
                    <button type="button" class="btn btn-success" @click="confirmPayment">Confirm Payment</button>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showPayment" class="modal-backdrop fade show"></div>
</div>

</template>

<style scoped>
</style>
