from models import db, User, Appointment, DoctorAvailability, PatientHistory
from datetime import datetime, timedelta

def get_dashboard_data(user_id):
    today_appointments = Appointment.query.filter(
        Appointment.status != 'cancelled',
        Appointment.doctor_id == user_id
    ).all()

    pending = Appointment.query.filter(
        Appointment.status == 'booked',
        Appointment.doctor_id == user_id
    ).all()

    completed = Appointment.query.filter(
        Appointment.status == 'completed',
        Appointment.doctor_id == user_id
    ).all()

    assigned_patients = User.query.join(Appointment, User.id == Appointment.patient_id).filter(
        Appointment.doctor_id == user_id
    ).distinct().all()

    total_cancelled = Appointment.query.filter(
        Appointment.status == 'cancelled',
        Appointment.doctor_id == user_id
    ).count()

    return {
        'today_appointments': [a.serialize() for a in today_appointments],
        'pending_appointments': [a.serialize() for a in pending],
        'completed_appointments': [a.serialize() for a in completed],
        'assigned_patients': [{'id': p.id, 'name': p.name} for p in assigned_patients],
        'stats': {
            'pending': len(pending),
            'completed': len(completed),
            'cancelled': total_cancelled
        }
    }


def complete_appointment(appointment_id, doctor_id):
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=doctor_id,
        status='booked'
    ).first()

    if not appointment:
        return False, "Appointment not found or already completed"

    try:
        appointment.status = 'completed'
        db.session.commit()
        return True, "Appointment completed successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Error completing appointment: {str(e)}"


def update_patient_history(appointment_id, doctor_id, visit_type, tests_done, diagnosis, prescription, medicines):
    appointment = Appointment.query.filter_by(id=appointment_id, doctor_id=doctor_id).first()

    if not appointment:
        return False, "Invalid appointment or not authorized"

    history_record = PatientHistory(
        appointment_id=appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=doctor_id,
        visit_type=visit_type,
        test_done=tests_done,
        diagnosis=diagnosis,
        prescription=prescription,
        medicines=medicines
    )

    try:
        db.session.add(history_record)
        db.session.commit()
        return True, "Patient history updated successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Error updating patient history: {str(e)}"


def get_availability_slots(doctor_id):
    dates = [(datetime.now() + timedelta(days=i)).strftime('%d %b') for i in range(7)]
    availability = {}

    for date in dates:
        date_obj = datetime.strptime(f"{date} {datetime.now().year}", '%d %b %Y').date()
        morning_slot = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj,
            time_slot='morning'
        ).first()
        evening_slot = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj,
            time_slot='evening'
        ).first()

        availability[date] = {
            'morning': 'available' if morning_slot and morning_slot.is_available else 'unavailable',
            'evening': 'available' if evening_slot and evening_slot.is_available else 'unavailable'
        }

    return dates, availability


def update_availability_slots(doctor_id, selected_slots, dates):
    for date_str in dates:
        date_obj = datetime.strptime(f"{date_str} {datetime.now().year}", '%d %b %Y').date()

        for time_slot in ['morning', 'evening']:
            key = f"{date_str}_{time_slot}"
            is_selected = key in selected_slots

            slot = DoctorAvailability.query.filter_by(
                doctor_id=doctor_id,
                date=date_obj,
                time_slot=time_slot
            ).first()

            if slot:
                slot.is_available = is_selected
            else:
                new_slot = DoctorAvailability(
                    doctor_id=doctor_id,
                    date=date_obj,
                    time_slot=time_slot,
                    is_available=is_selected
                )
                db.session.add(new_slot)

    try:
        db.session.commit()
        return True, "Availability updated successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Error updating availability: {str(e)}"


def reschedule_appointment(appointment_id, patient_id, new_date, new_time_slot):
    appointment = Appointment.query.get(appointment_id)

    if not appointment or appointment.patient_id != patient_id:
        return False, "Not authorized to reschedule this appointment"

    try:
        appointment.date = new_date
        appointment.time_slot = new_time_slot
        db.session.commit()
        return True, "Successfully rescheduled"
    except Exception as e:
        db.session.rollback()
        return False, f"Error rescheduling: {str(e)}"