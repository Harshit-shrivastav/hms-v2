import { createRouter, createWebHistory } from 'vue-router'

import LandingView from "../views/LandingView.vue"
import LoginView from "../views/LoginView.vue"
import ProfileView from "../views/ProfileView.vue"
import ErrorView from "../views/ErrorView.vue"
import PatientHistoryView from "../views/PatientHistoryView.vue"
import DoctorDetailsView from "../views/DoctorDetailsView.vue"

import AdminDashboardView from "../views/admin/DashboardView.vue"
import AdminAddDeptView from "../views/admin/AddDeptView.vue"
import AdminAddDoctorView from "../views/admin/AddDoctorView.vue"

import DoctorDashboardView from "../views/doctor/DashboardView.vue"
import DoctorSlotsView from "../views/doctor/SlotsView.vue"
import DoctorUpdateHistoryView from "../views/doctor/UpdateHistoryView.vue"
import DoctorPatientHistoryView from "../views/doctor/PatientHistoryView.vue"

import PatientDashboardView from "../views/patient/DashboardView.vue"
import PatientDepartmentView from "../views/patient/DepartmentView.vue"
import PatientRegisterView from "../views/patient/RegisterView.vue"
import PatientSearchDoctorsView from "../views/patient/SearchDoctorsView.vue"
import PatientBookSlotView from "../views/patient/BookSlotView.vue"
import PatientRescheduleView from "../views/patient/RescheduleView.vue"
import PatientMyHistoryView from "../views/patient/MyHistoryView.vue"

const routes = [
    { path: '/', name: 'Landing', component: LandingView },
    { path: '/login', name: 'Login', component: LoginView },
    { path: '/profile', name: 'Profile', component: ProfileView },
    { path: '/profile/:id', name: 'EditUserProfile', component: ProfileView },
    { path: '/error', name: 'Error', component: ErrorView },
    { path: '/patient-history', name: 'PatientHistory', component: PatientHistoryView },
    { path: '/patient-history/:patientId', name: 'PatientHistoryDetail', component: PatientHistoryView },
    { path: '/doctor/:id', name: 'DoctorDetails', component: DoctorDetailsView },

    { path: '/admin', name: 'AdminDashboard', component: AdminDashboardView },
    { path: '/admin/add-dept', name: 'AdminAddDept', component: AdminAddDeptView },
    { path: '/admin/add-doctor', name: 'AdminAddDoctor', component: AdminAddDoctorView },

    { path: '/doctor', name: 'DoctorDashboard', component: DoctorDashboardView },
    { path: '/doctor/slots', name: 'DoctorSlots', component: DoctorSlotsView },
    { path: '/doctor/update-history/:aptId', name: 'DoctorUpdateHistory', component: DoctorUpdateHistoryView },
    { path: '/doctor/patient-history/:patientId', name: 'DoctorPatientHistory', component: DoctorPatientHistoryView },

    { path: '/patient', name: 'PatientDashboard', component: PatientDashboardView },
    { path: '/patient/departments/:deptId', name: 'PatientDepartments', component: PatientDepartmentView },
    { path: '/patient/register', name: 'PatientRegister', component: PatientRegisterView },
    { path: '/patient/search-doctors', name: 'PatientSearchDoctors', component: PatientSearchDoctorsView },
    { path: '/patient/book-slot/:doctorId', name: 'PatientBookSlot', component: PatientBookSlotView },
    { path: '/patient/reschedule', name: 'PatientReschedule', component: PatientRescheduleView },
    { path: '/my-history', name: 'PatientMyHistory', component: PatientMyHistoryView },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router