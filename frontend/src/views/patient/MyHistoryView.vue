<script setup>
import { ref, onMounted } from 'vue'
import { patientService } from '../../services'

const histories = ref([])

const load = async () => {
  const res = await patientService.getMyHistory()
  histories.value = res.data
}

onMounted(load)
</script>

<template>
<div class="container mt-5">
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0">My Medical History</h3>
                </div>
                <div class="card-body">
                    <div v-if="!histories.length" class="text-center py-4">
                        <p class="text-muted">No medical history found</p>
                    </div>
                    <div v-else class="card mb-3" v-for="h in histories" :key="h.id">
                        <div class="card-header">
                            <h5 class="mb-0">
                                Visit: {{ h.visit_type }}
                                <small class="text-muted float-end">{{ h.visit_date }}</small>
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Doctor:</strong> {{ h.doctor_name }}</p>
                                    <p><strong>Tests Done:</strong></p>
                                    <p>{{ h.tests_done || 'N/A' }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Diagnosis:</strong></p>
                                    <p>{{ h.diagnosis || 'N/A' }}</p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Prescription:</strong></p>
                                    <p>{{ h.prescription || 'N/A' }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Medicines:</strong></p>
                                    <p>{{ h.medicines || 'N/A' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="text-center">
                        <a href="/patient" class="btn btn-primary">Back to Dashboard</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>
