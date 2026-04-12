<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { patientService } from '../../services'

const route = useRoute()
const doctors = ref([])
const deptName = ref('')

const load = async () => {
  const res = await patientService.getDoctorsByDepartment(route.params.deptId)
  doctors.value = res.data
  if (doctors.value.length > 0) {
    deptName.value = doctors.value[0]?.dept || 'Department'
  }
}

onMounted(load)
</script>

<template>
<div class="container-fluid">
    <div class="row">
        <main class="col-md-12 px-md-4">
            <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
                <h1 class="h2">{{ deptName }} Department</h1>
            </div>

            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Available Doctors</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Doctor Name</th>
                                    <th>Specialization</th>
                                    <th>Experience</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="doc in doctors" :key="doc.id">
                                    <td>{{ doc.name }}</td>
                                    <td>{{ doc.dept }}</td>
                                    <td>{{ doc.experience }} years</td>
                                    <td>
                                        <router-link :to="`/patient/book-slot/${doc.id}`">
                                            <button class="btn btn-sm btn-outline-primary me-1">Check Availability</button>
                                        </router-link>
                                         <router-link :to="`/doctor/${doc.id}`">
                                            <button class="btn btn-sm btn-outline-primary me-1">View Doctor</button>
                                        </router-link>
                                    </td>
                                </tr>
                                <tr v-if="doctors.length === 0">
                                    <td colspan="4" class="text-center text-muted">No doctors available</td>
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
