<script setup>
import { useRouter, useRoute } from 'vue-router'
import { doctorService } from "../services/index.js";
import { ref, onMounted } from "vue"

const name = ref('')
const dept = ref('')
const exp = ref('')
const id = ref('')

const route = useRoute()
const doctorId = route.params.id

onMounted(async () => {
  try {
    const res = await doctorService.getById(doctorId)
    const doctor = res.data
    name.value = doctor.name
    dept.value = doctor.dept
    exp.value = doctor.experience
    id.value = doctor.id
  } catch (e) {
    console.error(e)
  }
})

const router = useRouter()

const goback = () => {
  router.back()
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body text-center">
                        <div class="mb-4">
                            <i class="bi bi-person-circle" style="font-size: 8rem; color: #6c757d;"></i>
                        </div>
                        <h3 class="card-title">{{ name }}</h3>
                        <p class="card-text">
                            <strong>Experience:</strong> {{exp}} <br>
                            <strong>Dept:</strong> {{ dept }}
                        </p>
                        <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                           <router-link :to="`/patient/book-slot/${id}`" class="btn btn-primary me-md-2">Check Availability
                            </router-link>
                            <a href="#" @click.prevent="goback"> <button class="btn btn-secondary">Go Back</button> </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<style scoped>

</style>
