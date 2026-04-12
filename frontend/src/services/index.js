import api from './api'

export const authService = {
  login: (email, password) => {
    return api.post('/login', { email, password })
  },


  register: (name, email, username, password, gender, age) => {
    return api.post('/register', {name, username, gender, email, password, confirm_password: password, age})
  },

  logout: () => {
    return api.post('/logout')
  },

   isLoggedIn: () => {
    return api.get('/login-status')
  },

  getProfile: () => {
    return api.get('/patient/profile')
  },
}

export const doctorService = {
  getAll: () => {
    return api.get('/doctors')
  },

  getById: (id) => {
    return api.get(`/doctors/${id}`)
  },

  create: (data) => {
    return api.post('/admin/create-doctor', data)
  },

  update: (id, data) => {
    return api.put(`/doctors/${id}`, data)
  },

  delete: (id) => {
    return api.delete(`/doctors/${id}`)
  },

  getAvailability: () => {
    return api.get('/doctor/availability')
  },

  saveAvailability: (slots) => {
    return api.post('/doctor/availability', { slots })
  },

  getDashboard: () => {
    return api.get('/doctor/dashboard')
  },

  cancelAppointment: (aptId) => {
    return api.post(`/doctor/appointment/${aptId}/cancel`)
  },

  completeAppointment: (aptId) => {
    return api.post(`/doctor/appointment/${aptId}/complete`)
  },

  getAppointment: (aptId) => {
    return api.get(`/doctor/appointment/${aptId}`)
  },

  savePatientHistory: (data) => {
    return api.post('/doctor/patient-history', data)
  },

  getPatientHistory: (patientId) => {
    return api.get(`/doctor/patient/${patientId}/history`)
  },

  getAppointmentHistory: (aptId) => {
    return api.get(`/doctor/appointment/${aptId}/history`)
  },
}

export const patientService = {
    getPatientDashboard: () => {
    return api.get('/patient')
  },

  getProfile: () => {
    return api.get('/patient/profile')
  },

  updateProfile: (data) => {
    return api.put('/patient/profile', data)
  },

  getDepartments: () => {
    return api.get('/patient/departments')
  },

  getDoctorsByDepartment: (deptId) => {
    return api.get(`/patient/doctors/${deptId}`)
  },

  getDoctorSlots: (doctorId) => {
    return api.get(`/patient/doctor/${doctorId}/slots`)
  },

  bookAppointment: (doctorId, date, timeSlot) => {
    return api.post('/patient/book-appointment', { doctor_id: doctorId, date, time_slot: timeSlot })
  },

  bookAppointmentData: (data) => {
    return api.post('/appointments', data)
  },

  getAppointments: () => {
    return api.get('/appointments')
  },

  rescheduleAppointment: (id, data) => {
    return api.put(`/appointments/${id}`, data)
  },

  cancelAppointment: (appointmentId) => {
    return api.post('/cancel-appointment', { appointment_id: appointmentId })
  },

  getMyHistory: () => {
    return api.get('/patient/my-history')
  },

  searchDoctors: (name, deptId) => {
    const params = {}
    if (name) params.name = name
    if (deptId) params.dept_id = deptId
    return api.get('/patient/search-doctors', { params })
  },

  exportPatientData: () => {
    return api.post('/patient/export')
  },
}

export const adminService = {
  getDashboard: () => {
    return api.get('/admin/dashboard')
  },

  createDepartment: (data) => {
    return api.post('admin/create-department', data)
  },

  getDepartments: () => {
    return api.get('/admin/get-departments')
  },

  blockUser: (userId) => {
    return api.put(`/admin/block-user/${userId}`)
  },

  deleteUser: (userId) => {
    return api.delete(`/admin/delete-user/${userId}`)
  },

  getUser: (userId) => {
    return api.get(`/admin/user/${userId}`)
  },

  updateUser: (userId, data) => {
    return api.put(`/admin/user/${userId}`, data)
  },

  getPatientHistory: (patientId) => {
    return api.get(`/admin/patient/${patientId}/history`)
  },
}
