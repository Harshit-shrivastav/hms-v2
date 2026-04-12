<script setup>
import { ref, onMounted } from 'vue'
import { doctorService } from '../../services'

const dates = ref([])
const availability = ref({})
const loading = ref(false)
const message = ref('')

const loadAvailability = async () => {
  loading.value = true
  try {
    const res = await doctorService.getAvailability()
    dates.value = res.data.dates
    availability.value = res.data.availability
  } catch (err) {
    console.error('Error loading availability:', err)
  } finally {
    loading.value = false
  }
}

const isAvailable = (dateStr, slot) => {
  return availability.value[dateStr]?.[slot] ?? false
}

const toggleSlot = (dateStr, slot) => {
  if (!availability.value[dateStr]) {
    availability.value[dateStr] = { morning: false, evening: false }
  }
  availability.value[dateStr][slot] = !availability.value[dateStr][slot]
}

const saveAvailability = async () => {
  loading.value = true
  message.value = ''
  try {
    const slots = []
    Object.keys(availability.value).forEach(dateStr => {
      slots.push(
        { date: dateStr, time_slot: 'morning', is_available: availability.value[dateStr].morning },
        { date: dateStr, time_slot: 'evening', is_available: availability.value[dateStr].evening }
      )
    })
    await doctorService.saveAvailability(slots)
    message.value = 'Availability saved successfully!'
  } catch (err) {
    message.value = err.response?.data?.msg || 'Failed to save availability'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAvailability()
})
</script>

<template>
<div class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="text-center mb-4">
                    <h1 class="display-5 fw-bold text-primary">Doctors Availability</h1>
                    <p class="lead text-muted">Select time slots for the next 7 days</p>
                </div>
                
                <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
                    {{ message }}
                </div>
                
                <div class="card shadow-sm">
                    <div class="card-body p-4">

                        <div class="table-responsive">
                            <table class="table table-borderless">
                                <thead>
                                    <tr>
                                        <th class="text-center">Date</th>
                                        <th class="text-center">9:00 AM - 1:00 PM</th>
                                        <th class="text-center">3:00 PM - 7:00 PM</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="dateStr in dates" :key="dateStr">
                                        <td class="align-middle text-center">
                                            <span class="fw-bold">{{ dateStr }}</span>
                                        </td>
                                        <td class="align-middle">
                                            <div 
                                                class="border p-3 rounded text-center cursor-pointer"
                                                :class="isAvailable(dateStr, 'morning') ? 'bg-success bg-opacity-10 border-success' : 'bg-danger bg-opacity-10 border-danger'"
                                                @click="toggleSlot(dateStr, 'morning')"
                                            >
                                                <input 
                                                    type="checkbox" 
                                                    :checked="isAvailable(dateStr, 'morning')"
                                                    class="me-2 pointer-events-none"
                                                >
                                                <span :class="isAvailable(dateStr, 'morning') ? 'text-success' : 'text-danger'">
                                                    9:00 AM - 1:00 PM
                                                </span>
                                            </div>
                                        </td>
                                        <td class="align-middle">
                                            <div 
                                                class="border p-3 rounded text-center cursor-pointer"
                                                :class="isAvailable(dateStr, 'evening') ? 'bg-success bg-opacity-10 border-success' : 'bg-danger bg-opacity-10 border-danger'"
                                                @click="toggleSlot(dateStr, 'evening')"
                                            >
                                                <input 
                                                    type="checkbox" 
                                                    :checked="isAvailable(dateStr, 'evening')"
                                                    class="me-2 pointer-events-none"
                                                >
                                                <span :class="isAvailable(dateStr, 'evening') ? 'text-success' : 'text-danger'">
                                                    3:00 PM - 7:00 PM
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="d-flex justify-content-center mt-4">
                            <button
                                type="button"
                                class="btn btn-primary px-5 py-2"
                                @click="saveAvailability"
                                :disabled="loading"
                            >
                                Save Availability
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<style scoped>
</style>
