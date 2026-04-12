from models import db, User, Appointment


def get_dashboard_data(user_id):
    doc_dept = [
        dept[0]
        for dept in db.session.query(User.dept).distinct().all()
        if dept[0] is not None
    ]

    upcoming = Appointment.query.filter_by(status="booked", patient_id=user_id).all()
    total = Appointment.query.filter_by(patient_id=user_id).all()
    completed = Appointment.query.filter_by(
        status="completed", patient_id=user_id
    ).all()
    cancelled = Appointment.query.filter_by(
        status="cancelled", patient_id=user_id
    ).all()

    return {
        "departments": doc_dept,
        "upcoming_appointments": [a.serialize() for a in upcoming],
        "total_appointments": len(total),
        "completed_appointments": len(completed),
        "cancelled_appointments": len(cancelled),
    }


def get_patient_history(patient_id, current_user_id, current_user_role):
    if current_user_role == "doctor":
        history_records = (
            PatientHistory.query.filter_by(
                patient_id=patient_id, doctor_id=current_user_id
            )
            .order_by(PatientHistory.visit_date.desc())
            .all()
        )
    elif current_user_role == "patient":
        history_records = (
            PatientHistory.query.filter_by(patient_id=current_user_id)
            .order_by(PatientHistory.visit_date.desc())
            .all()
        )
    else:  # admin
        history_records = (
            PatientHistory.query.filter_by(patient_id=patient_id)
            .order_by(PatientHistory.visit_date.desc())
            .all()
        )

    patient = User.query.get_or_404(patient_id)
    return history_records, patient


def cancel_appointment(appointment_id, user_id, user_role):
    if user_role == "doctor":
        appointment = Appointment.query.filter_by(
            id=appointment_id, doctor_id=user_id, status="booked"
        ).first()
    else:
        appointment = Appointment.query.filter_by(
            id=appointment_id, patient_id=user_id, status="booked"
        ).first()

    if not appointment:
        return False, "Appointment not found or already cancelled"

    try:
        appointment.status = "cancelled"
        db.session.commit()
        return True, "Appointment cancelled successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Error cancelling appointment: {str(e)}"


def book_appointment(patient_id, doctor_id, date_obj, time_slot):
    doctor = User.query.filter_by(id=doctor_id, role="doctor").first()
    if not doctor:
        return False, "Doctor not found"

    existing = Appointment.query.filter_by(
        patient_id=patient_id, date=date_obj, time_slot=time_slot, status="booked"
    ).first()

    if existing:
        return False, "You already have an appointment booked for this slot."

    availability = DoctorAvailability.query.filter_by(
        doctor_id=doctor_id, date=date_obj, time_slot=time_slot
    ).first()

    if not availability or not availability.is_available:
        return False, "Selected slot is no longer available"

    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=date_obj,
        time_slot=time_slot,
        doc_dept=doctor.dept,
        doc_name=doctor.name,
    )

    try:
        db.session.add(new_appointment)
        db.session.commit()
        return True, "Slot successfully booked"
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"


def search_doctors(dept="", date_str="", time_slot="", doctor_name=""):
    doctors = User.query.filter_by(role="doctor")

    if doctor_name:
        doctors = doctors.filter(User.name.ilike(f"%{doctor_name}%"))
    else:
        if dept:
            doctors = doctors.filter(User.dept == dept)
        doctors = doctors.all()

    availability_info = {}
    searched_date = None

    if date_str:
        try:
            from datetime import datetime

            searched_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            avails = DoctorAvailability.query.filter_by(date=searched_date).all()
            for a in avails:
                if a.doctor_id not in availability_info:
                    availability_info[a.doctor_id] = {
                        "morning": "unavailable",
                        "evening": "unavailable",
                    }
                availability_info[a.doctor_id][a.time_slot] = (
                    "available" if a.is_available else "unavailable"
                )
        except Exception as e:
            print(e)

    if searched_date and time_slot in ("morning", "evening"):
        doctors = [
            d
            for d in doctors
            if availability_info.get(d.id, {}).get(time_slot) == "available"
        ]

    return doctors, availability_info, searched_date
