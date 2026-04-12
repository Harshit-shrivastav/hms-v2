from flask import jsonify, request
from app import flask_app as app, db, cache
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime, timedelta
from app.models.models import User, DoctorAvailability, Department, Appointment, PatientHistory
from app.services.decorators import role_required


@app.get('/api/patient')
@jwt_required()
@role_required('patient')
def get_patients():
    depts = Department.query.all()
    appointments = Appointment.query.all()
    total_departments = len(depts)
    total_appointments = len(appointments)
    completed_appointments = Appointment.query.filter_by(status='completed').all()
    upcoming_appointments = Appointment.query.filter_by(status='booked').all()
    cancelled_appointments = Appointment.query.filter_by(status='cancelled').all()
    return jsonify({
        'data': {
            'total_departments': total_departments,
            'total_appointments': total_appointments,
            'completed_appointments': len(completed_appointments),
            'upcoming_appointments': len(upcoming_appointments),
            'cancelled_appointments': len(cancelled_appointments)
        }
    })

@app.get('/api/patient/departments')
@jwt_required()
@role_required('patient')
@cache.cached(timeout=600)
def get_patient_departments():
    depts = Department.query.all()
    return jsonify([{'id': d.id, 'name': d.depts} for d in depts]), 200


@app.get('/api/patient/doctors/<int:dept_id>')
@jwt_required()
@role_required('patient')
def get_doctors_by_department(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return jsonify([]), 200
    doctors = User.query.filter_by(role='doctor', dept=dept.depts).all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'dept': d.dept,
        'experience': d.experience
    } for d in doctors]), 200


@app.get('/api/patient/search-doctors')
@jwt_required()
@role_required('patient')
def search_doctors():
    name = request.args.get('name', '')
    dept_id = request.args.get('dept_id', '')
    doctors = User.query.filter_by(role='doctor').all()
    if name:
        doctors = [d for d in doctors if name.lower() in d.name.lower()]
    if dept_id:
        dept = Department.query.get(dept_id)
        if dept:
            doctors = [d for d in doctors if d.dept == dept.depts]
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'dept': d.dept,
        'experience': d.experience
    } for d in doctors]), 200


@app.get('/api/patient/doctor/<int:doctor_id>/slots')
@jwt_required()
@role_required('patient')
def get_doctor_slots(doctor_id):
    today = datetime.utcnow().date()
    dates = []
    availability = {}

    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime('%d %b %Y')
        dates.append(date_str)

        morning_avail = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, date=date, time_slot='morning', is_available=True
        ).first()
        evening_avail = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, date=date, time_slot='evening', is_available=True
        ).first()

        morning_booked = Appointment.query.filter_by(
            doctor_id=doctor_id, date=date, time_slot='morning', status='booked'
        ).first()
        evening_booked = Appointment.query.filter_by(
            doctor_id=doctor_id, date=date, time_slot='evening', status='booked'
        ).first()

        availability[date_str] = {
            'morning': morning_avail is not None and morning_booked is None,
            'evening': evening_avail is not None and evening_booked is None
        }

    return jsonify({'dates': dates, 'availability': availability}), 200


@app.post('/api/patient/book-appointment')
@jwt_required()
@role_required('patient')
def book_appointment():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    doctor_id = data.get('doctor_id')
    date_str = data.get('date')
    time_slot = data.get('time_slot')
    
    if not all([doctor_id, date_str, time_slot]):
        return jsonify({'msg': 'Missing required fields'}), 400
    
    date = datetime.strptime(date_str, '%d %b %Y').date()
    
    availability = DoctorAvailability.query.filter_by(
        doctor_id=doctor_id, date=date, time_slot=time_slot, is_available=True
    ).first()
    
    if not availability:
        return jsonify({'msg': 'Slot not available'}), 400
    
    existing = Appointment.query.filter_by(
        patient_id=current_user_id, doctor_id=doctor_id, date=date, time_slot=time_slot, status='booked'
    ).first()

    if existing:
        return jsonify({'msg': 'Appointment already booked for this slot'}), 400

    doctor = User.query.get(doctor_id)

    appointment = Appointment(
        patient_id=current_user_id,
        doctor_id=doctor_id,
        date=date,
        time_slot=time_slot,
        doc_dept=doctor.dept,
        doc_name=doctor.name
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'msg': 'Appointment booked successfully', 'id': appointment.id}), 201


@app.get('/api/patient/my-history')
@jwt_required()
@role_required('patient')
def get_my_history():
    current_user_id = get_jwt_identity()
    histories = PatientHistory.query.filter_by(patient_id=current_user_id).order_by(PatientHistory.visit_date.desc()).all()

    return jsonify([{
        'id': h.id,
        'appointment_id': h.appointment_id,
        'visit_type': h.visit_type,
        'tests_done': h.test_done,
        'diagnosis': h.diagnosis,
        'prescription': h.prescription,
        'medicines': h.medicines,
        'visit_date': h.visit_date.strftime('%Y-%m-%d %I:%M %p'),
        'doctor_name': h.doctor.name if h.doctor else 'Unknown'
    } for h in histories]), 200


@app.put('/api/appointments/<int:apt_id>')
@jwt_required()
@role_required('patient')
def reschedule_appointment(apt_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    date_str = data.get('date')
    time_slot = data.get('time_slot')

    if not all([date_str, time_slot]):
        return jsonify({'msg': 'Date and time slot are required'}), 400

    appointment = Appointment.query.filter_by(
        id=apt_id,
        patient_id=current_user_id,
        status='booked'
    ).first()

    if not appointment:
        return jsonify({'msg': 'Appointment not found or not in booked status'}), 404

    date = datetime.strptime(date_str, '%d %b %Y').date()

    availability = DoctorAvailability.query.filter_by(
        doctor_id=appointment.doctor_id,
        date=date,
        time_slot=time_slot,
        is_available=True
    ).first()

    if not availability:
        return jsonify({'msg': 'Slot not available for the selected date/time'}), 400

    existing = Appointment.query.filter_by(
        patient_id=current_user_id,
        doctor_id=appointment.doctor_id,
        date=date,
        time_slot=time_slot,
        status='booked'
    ).first()

    if existing:
        return jsonify({'msg': 'You already have an appointment booked for this slot'}), 400

    appointment.date = date
    appointment.time_slot = time_slot
    db.session.commit()

    return jsonify({'msg': 'Appointment rescheduled successfully'}), 200

