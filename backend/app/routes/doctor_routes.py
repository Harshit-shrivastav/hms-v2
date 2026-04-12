from flask import jsonify, request
from app import flask_app as app, db, cache
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
from app.models.models import User, DoctorAvailability, Appointment, PatientHistory
from app.services.decorators import role_required


@app.get('/api/doctor/dashboard')
@role_required('doctor')
def get_doctor_dashboard():
    current_user_id = get_jwt_identity()
    today = datetime.utcnow().date()

    all_appointments = Appointment.query.filter_by(doctor_id=current_user_id).all()
    today_appointments = [a for a in all_appointments if a.date == today]
    pending = Appointment.query.filter_by(doctor_id=current_user_id, status='booked').all()
    completed = Appointment.query.filter_by(doctor_id=current_user_id, status='completed').all()
    cancelled = Appointment.query.filter_by(doctor_id=current_user_id, status='cancelled').all()

    patient_ids = set(a.patient_id for a in all_appointments)
    assigned_patients = User.query.filter(User.id.in_(patient_ids)).all() if patient_ids else []

    return jsonify({
        'today_count': len(today_appointments),
        'pending_count': len(pending),
        'completed_count': len(completed),
        'cancelled_count': len(cancelled),
        'assigned_count': len(assigned_patients),
        'appointments': [{
            'id': a.id,
            'patient_name': a.patient.name,
            'date': a.date.strftime('%d %b'),
            'time_slot': a.time_slot,
            'status': a.status
        } for a in all_appointments if a.status == 'booked'],
        'patients': [{
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'email': p.email
        } for p in assigned_patients]
    }), 200


@app.post('/api/doctor/appointment/<int:apt_id>/cancel')
@role_required('doctor')
def doctor_cancel_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    apt.status = 'cancelled'
    db.session.commit()
    return jsonify({'msg': 'Appointment cancelled'}), 200


@app.post('/api/doctor/appointment/<int:apt_id>/complete')
@role_required('doctor')
def doctor_complete_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    apt.status = 'completed'
    db.session.commit()
    return jsonify({'msg': 'Appointment completed'}), 200


@app.get('/api/doctor/appointment/<int:apt_id>')
@role_required('doctor')
def get_appointment_details(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    return jsonify({
        'id': apt.id,
        'patient_id': apt.patient_id,
        'patient_name': apt.patient.name,
        'patient_age': apt.patient.age,
        'date': apt.date.strftime('%d %b %Y'),
        'time_slot': apt.time_slot,
        'department': apt.doc_dept
    }), 200


@app.post('/api/doctor/patient-history')
@role_required('doctor')
def save_patient_history():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    history = PatientHistory(
        appointment_id=data.get('appointment_id'),
        patient_id=data.get('patient_id'),
        doctor_id=current_user_id,
        visit_type=data.get('visit_type'),
        test_done=data.get('tests_done'),
        diagnosis=data.get('diagnosis'),
        prescription=data.get('prescription'),
        medicines=data.get('medicines')
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({'msg': 'Patient history saved'}), 201


@app.get('/api/doctor/patient/<int:patient_id>/history')
@role_required('doctor')
def get_patient_history(patient_id):
    histories = PatientHistory.query.filter_by(patient_id=patient_id).order_by(PatientHistory.visit_date.desc()).all()
    patient = User.query.get(patient_id)
    return jsonify({
        'patient_name': patient.name if patient else 'Patient',
        'history': [{
            'id': h.id,
            'visit_type': h.visit_type,
            'tests_done': h.test_done,
            'diagnosis': h.diagnosis,
            'prescription': h.prescription,
            'medicines': h.medicines,
            'visit_date': h.visit_date.strftime('%Y-%m-%d %I:%M %p'),
            'doctor_name': h.doctor.name if h.doctor else 'Unknown',
            'appointment_id': h.appointment_id
        } for h in histories]
    }), 200


@app.get('/api/doctor/appointment/<int:apt_id>/history')
@role_required('doctor')
def get_appointment_history(apt_id):
    history = PatientHistory.query.filter_by(appointment_id=apt_id).first()
    if history:
        return jsonify({
            'id': history.id,
            'visit_type': history.visit_type,
            'tests_done': history.test_done,
            'diagnosis': history.diagnosis,
            'prescription': history.prescription,
            'medicines': history.medicines
        }), 200
    return jsonify({}), 200


@app.get('/api/doctor/availability')
@role_required('doctor')
def get_doctor_availability():
    current_user_id = get_jwt_identity()
    today = datetime.utcnow().date()
    
    dates = []
    availability = {}
    
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime('%d %b %Y')
        dates.append(date_str)
        
        morning = DoctorAvailability.query.filter_by(
            doctor_id=current_user_id, date=date, time_slot='morning'
        ).first()
        evening = DoctorAvailability.query.filter_by(
            doctor_id=current_user_id, date=date, time_slot='evening'
        ).first()
        
        availability[date_str] = {
            'morning': morning.is_available if morning else False,
            'evening': evening.is_available if evening else False
        }
    
    return jsonify({'dates': dates, 'availability': availability}), 200


@app.post('/api/doctor/availability')
@role_required('doctor')
def save_doctor_availability():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    for slot in data.get('slots', []):
        date_str = slot['date']
        date = datetime.strptime(date_str, '%d %b %Y').date()
        time_slot = slot['time_slot']
        is_available = slot['is_available']
        
        availability = DoctorAvailability.query.filter_by(
            doctor_id=current_user_id, date=date, time_slot=time_slot
        ).first()
        
        if availability:
            availability.is_available = is_available
        else:
            db.session.add(DoctorAvailability(
                doctor_id=current_user_id,
                date=date,
                time_slot=time_slot,
                is_available=is_available
            ))
    
    db.session.commit()
    return jsonify({"msg": "Availability saved successfully"}), 200
