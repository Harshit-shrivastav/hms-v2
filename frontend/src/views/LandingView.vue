<script setup>

</script>

<template>
    <section class="hero" id="home">
        <div class="container">
            <h1 class="display-4 fw-bold mb-3">Hospital Management System</h1>
            <p class="lead mb-4">A complete hospital management system using vue.js, flask and redis.</p>
            <a href="#contact" class="btn btn-warning btn-lg">Get Started</a>
        </div>
    </section>
    <section id="features" class="py-5 bg-light">
        <div class="container">
            <h2 class="text-center mb-5 fw-bold">Key Features</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-person-badge feature-icon"></i>
                            <h5 class="card-title">Doctor Management</h5>
                            <p class="card-text">Doctor dashboard with patients management</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-hospital feature-icon"></i>
                            <h5 class="card-title">Patient Records</h5>
                            <p class="card-text">Patient dashboard for appointment booking, and other management.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-calendar-check feature-icon"></i>
                            <h5 class="card-title">Appointments</h5>
                            <p class="card-text">Simple appointment scheduling system</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-prescription feature-icon"></i>
                            <h5 class="card-title">Prescriptions</h5>
                            <p class="card-text">Digital prescription taking with history</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-bar-chart feature-icon"></i>
                            <h5 class="card-title">Reports</h5>
                            <p class="card-text">Automated reports on email</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="bi bi-shield-lock feature-icon"></i>
                            <h5 class="card-title">Admin Panel</h5>
                            <p class="card-text">Admin panel with complete user and doctor management</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="services" class="py-5">
        <div class="container">
            <h2 class="text-center mb-5 fw-bold">Our Services</h2>
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="alert alert-info border-start border-4" role="alert">
                        <i class="bi bi-exclamation-triangle"></i>
                        <h5 class="alert-heading d-inline-block ms-2">Emergency Services</h5>
                        <p class="mt-2 mb-0">Our services are available at whole day and night</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="alert alert-info border-start border-4" role="alert">
                        <i class="bi bi-clipboard-check"></i>
                        <h5 class="alert-heading d-inline-block ms-2">Complete Care</h5>
                        <p class="mt-2 mb-0">We provide complete care of patients</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="alert alert-info border-start border-4" role="alert">
                        <i class="bi bi-building">Emergency medicines</i>
                        <h5 class="alert-heading d-inline-block ms-2"></h5>
                        <p class="mt-2 mb-0">We provide emergency medicines at hospitaal</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="alert alert-info border-start border-4" role="alert">
                        <i class="bi bi-microscope"></i>
                        <h5 class="alert-heading d-inline-block ms-2">Laboratory Tests</h5>
                        <p class="mt-2 mb-0">We have Labs for various types of testings</p>
                    </div>
                </div>


            </div>
        </div>
    </section>

    <section id="contact" class="py-5 bg-light">
        <div class="container">
            <h2 class="text-center mb-5 fw-bold">Contact Us</h2>
            <div class="row text-center g-4">
                <div class="col-md-3">
                    <div class="card border-0 h-100">
                        <div class="card-body">
                            <i class="bi bi-telephone" style="font-size: 2rem; color: #66ead6;"></i>
                            <h5 class="card-title mt-3">Phone</h5>
                            <p class="card-text">+91 9876543210</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card border-0 h-100">
                        <div class="card-body">
                            <i class="bi bi-envelope" style="font-size: 2rem; color: #66eac7;"></i>
                            <h5 class="card-title mt-3">Email</h5>
                            <p class="card-text">info@hms.com</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card border-0 h-100">
                        <div class="card-body">
                            <i class="bi bi-geo-alt" style="font-size: 2rem; color: #66ea9f;"></i>
                            <h5 class="card-title mt-3">Address</h5>
                            <p class="card-text">123, delhi India</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card border-0 h-100">
                        <div class="card-body">
                            <i class="bi bi-clock" style="font-size: 2rem; color: #66ea8b;"></i>
                            <h5 class="card-title mt-3">Hours</h5>
                            <p class="card-text">24/7 Service</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.hero {
    background: linear-gradient(135deg, #1dedaf 0%, #ffffff 100%);
            color: white;
            padding: 80px 0;
            text-align: center;
        }
.feature-icon {
            font-size: 3rem;
            color: #08edaf;
            margin-bottom: 1rem;
        }


</style>