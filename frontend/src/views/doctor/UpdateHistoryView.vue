<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { doctorService } from '../../services'

const route = useRoute()
const router = useRouter()
const apt = ref(null)
const loading = ref(false)
const msg = ref('')
const msgType = ref('')
const form = ref({})

const load = async () => {
  const res = await doctorService.getAppointment(route.params.aptId)
  apt.value = res.data
  form.value = {
    appointment_id: route.params.aptId,
    patient_id: res.data.patient_id,
    visit_type: '',
    tests_done: '',
    diagnosis: '',
    prescription: '',
    medicines: ''
  }
  
  const aptHistory = await doctorService.getAppointmentHistory(route.params.aptId)
  if (aptHistory.data && aptHistory.data.id) {
    form.value = {
      appointment_id: route.params.aptId,
      patient_id: res.data.patient_id,
      visit_type: aptHistory.data.visit_type,
      tests_done: aptHistory.data.tests_done,
      diagnosis: aptHistory.data.diagnosis,
      prescription: aptHistory.data.prescription,
      medicines: aptHistory.data.medicines
    }
  }
}

const submit = async () => {
  loading.value = true
  try {
    await doctorService.savePatientHistory(form.value)
    msg.value = 'History saved!'
    msgType.value = 'success'
    await load()
  } catch (e) {
    msg.value = e.response?.data?.msg || 'Failed'
    msgType.value = 'danger'
  }
  loading.value = false
}

const timeLabel = (slot) => slot === 'morning' ? '9AM-1PM' : '3PM-7PM'

onMounted(load)
</script>

<template>
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0">Update Patient History</h3>
                </div>
                <div class="card-body">
                    <div v-if="msg" :class="`alert alert-${msgType}`">{{ msg }}</div>

                    <div class="mb-4" v-if="apt">
                        <h5>Patient: {{ apt.patient_name }}</h5>
                        <h6>Appointment Date: {{ apt.date }} - {{ timeLabel(apt.time_slot) }}</h6>
                        <h6>Department: {{ apt.department }}</h6>
                    </div>

                    <form @submit.prevent="submit">
                        <div class="mb-3">
                            <label for="visit_type" class="form-label">Visit Type</label>
                            <select class="form-select" id="visit_type" v-model="form.visit_type" required>
                                <option value="">Select Visit Type</option>
                                <option value="First Visit">First Visit</option>
                                <option value="Follow-up">Follow-up</option>
                                <option value="Emergency">Emergency</option>
                                <option value="Consultation">Consultation</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="tests_done" class="form-label">Tests Done</label>
                            <textarea class="form-control" id="tests_done" v-model="form.tests_done" rows="2" placeholder="Enter tests performed..."></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="diagnosis" class="form-label">Diagnosis</label>
                            <textarea class="form-control" id="diagnosis" v-model="form.diagnosis" rows="3" placeholder="Enter diagnosis..." required></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="prescription" class="form-label">Prescription</label>
                            <textarea class="form-control" id="prescription" v-model="form.prescription" rows="3" placeholder="Enter prescription details..."></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="medicines" class="form-label">Medicines</label>
                            <textarea class="form-control" id="medicines" v-model="form.medicines" rows="2" placeholder="List medicines prescribed..."></textarea>
                        </div>

                        <div class="d-flex gap-2 d-md-flex justify-content-md-end">
                            <a href="/doctor" class="btn btn-secondary me-md-2">Cancel</a>
                            <button type="submit" class="btn btn-success" :disabled="loading">Save</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

</template>
