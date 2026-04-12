from app.models.models import db, User, Appointment, Department
from werkzeug.security import generate_password_hash


def get_dashboard_stats():
    doctors = User.query.filter(User.role.in_(["doctor", "BLOCKED_doctor"])).all()
    patients = User.query.filter(User.role.in_(["patient", "BLOCKED_patient"])).all()

    all_appointments = Appointment.query.all()
    pending_appointments = [a for a in all_appointments if a.status == "booked"]
    completed_appointments = [a for a in all_appointments if a.status == "completed"]

    return {
        "total_doctors": len(doctors),
        "total_patients": len(patients),
        "patients": [
            {"id": p.id, "name": p.name, "age": p.age, "email": p.email, "role": p.role}
            for p in patients
        ],
        "doctors": [
            {
                "id": d.id,
                "name": d.name,
                "dept": d.dept,
                "experience": d.experience,
                "role": d.role,
            }
            for d in doctors
        ],
        "pending_appointments_count": len(pending_appointments),
        "completed_appointments_count": len(completed_appointments),
        "total_appointments": len(all_appointments),
        "appointments": [
            {
                "id": a.id,
                "patient_name": a.patient.name,
                "patient_id": a.patient_id,
                "doctor_name": a.doc_name,
                "department": a.doc_dept,
                "date": a.date.strftime("%d %b %Y"),
                "time_slot": a.time_slot,
                "status": a.status,
            }
            for a in pending_appointments[:10]
        ],
        "past_appointments": [
            {
                "id": a.id,
                "patient_name": a.patient.name,
                "patient_id": a.patient_id,
                "doctor_name": a.doc_name,
                "department": a.doc_dept,
                "date": a.date.strftime("%d %b %Y"),
                "time_slot": a.time_slot,
                "status": a.status,
            }
            for a in completed_appointments[:10]
        ],
    }


def create_doctor(full_name, department, experience, email, mobile, username, password):
    if len(password) < 5:
        return False, "Password should be at least 5 characters.", None

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        return False, "Username or email already exists.", None

    mobile_num = None
    if mobile:
        try:
            mobile_num = int(mobile)
        except (ValueError, TypeError):
            pass

    exp_str = None
    if experience:
        try:
            exp_str = str(int(experience))
        except (ValueError, TypeError):
            exp_str = str(experience)

    new_doctor = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        name=full_name,
        role="doctor",
        mobile=mobile_num,
        dept=department,
        experience=exp_str,
    )

    try:
        db.session.add(new_doctor)
        db.session.commit()
        return True, "Doctor added successfully!", new_doctor
    except Exception as e:
        db.session.rollback()
        print(f"Error creating doctor: {str(e)}")
        return False, f"An error occurred: {str(e)}", None


def add_department(department_name):
    department_name = department_name.strip()
    if not department_name:
        return False, "Department name cannot be empty."

    exists = Department.query.filter_by(depts=department_name).first()
    if exists:
        return False, "Department already exists."

    try:
        new_dept = Department(depts=department_name)
        db.session.add(new_dept)
        db.session.commit()
        return True, "Department added."
    except Exception as e:
        db.session.rollback()
        return False, f"Error adding department: {str(e)}"


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found."

    if user.role == "admin":
        return False, "Cannot delete admin users."

    active_appointments = Appointment.query.filter(
        ((Appointment.patient_id == user_id) | (Appointment.doctor_id == user_id))
        & (Appointment.status == "booked")
    ).count()

    if active_appointments > 0:
        return False, "Cannot delete user with active appointments."

    try:
        db.session.delete(user)
        db.session.commit()
        return True, f"{user.name} has been deleted successfully."
    except Exception as e:
        db.session.rollback()
        return False, f"Error deleting user: {str(e)}"


def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found."

    if user.role == "admin":
        return False, "Cannot block admin users."

    try:
        if user.role.startswith("BLOCKED_"):
            user.role = user.role.replace("BLOCKED_", "")
            msg = f"{user.name} has been unblocked."
        else:
            user.role = f"BLOCKED_{user.role}"
            msg = f"{user.name} has been blocked."

        db.session.commit()
        return True, msg
    except Exception as e:
        db.session.rollback()
        return False, f"Error updating user status: {str(e)}"


def get_all_departments():
    return Department.query.all()
