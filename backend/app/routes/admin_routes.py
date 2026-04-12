from flask import jsonify, request
from app import flask_app as app, db, cache
from flask_jwt_extended import jwt_required
from app.services.admin_services import (
    get_dashboard_stats,
    create_doctor,
    add_department,
    get_all_departments,
    delete_user,
    block_user,
)
from app.models.models import User, PatientHistory
from werkzeug.security import generate_password_hash


@app.get("/api/admin/dashboard")
@jwt_required()
def admin_dashboard():
    data = get_dashboard_stats()
    return jsonify(data)


@app.post("/api/admin/create-department")
@jwt_required()
def create_department():
    data = request.get_json()
    dept_name = data.get("name", "")

    success, msg = add_department(dept_name)

    if success:
        cache.clear()
        return jsonify({"msg": msg}), 201
    else:
        return jsonify({"msg": msg}), 400


@app.get("/api/admin/get-departments")
@jwt_required()
@cache.cached(timeout=60)
def admin_get_departments():
    departments = get_all_departments()
    return jsonify(
        {"departments": [{"id": d.id, "name": d.depts} for d in departments]}
    )


@app.post("/api/admin/create-doctor")
@jwt_required()
def add_doctor():
    data = request.get_json()

    full_name = data.get("full_name", "")
    department = data.get("department", "")
    experience = data.get("experience", "")
    email = data.get("email", "")
    mobile = data.get("mobile", "")
    username = data.get("username", "")
    password = data.get("password", "")

    success, msg, _ = create_doctor(
        full_name, department, experience, email, mobile, username, password
    )

    if success:
        return jsonify({"msg": msg}), 201
    else:
        return jsonify({"msg": msg}), 400


@app.get("/api/admin/user/<int:user_id>")
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found."}), 404
    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "gender": user.gender or "",
            "age": user.age or "",
            "experience": user.experience or "",
            "dept": user.dept or "",
        }
    )


@app.put("/api/admin/user/<int:user_id>")
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided."}), 400

    if "name" in data:
        user.name = data["name"]

    if "email" in data:
        existing_user = User.query.filter(
            User.email == data["email"], User.id != user_id
        ).first()
        if existing_user:
            return jsonify({"msg": "Email already in use."}), 400
        user.email = data["email"]

    if "gender" in data:
        user.gender = data["gender"]

    if "age" in data:
        age = data["age"]
        if age == "" or age is None:
            pass
        else:
            try:
                age = int(age)
                if age < 0 or age > 150:
                    return jsonify({"msg": "Age must be between 0 and 150."}), 400
                user.age = age
            except (ValueError, TypeError):
                return jsonify({"msg": "Age must be a valid number."}), 400

    if "experience" in data:
        user.experience = data["experience"]

    if "dept" in data:
        user.dept = data["dept"]

    db.session.commit()

    return jsonify(
        {
            "msg": "Profile updated successfully",
            "data": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "gender": user.gender,
                "age": user.age,
                "experience": user.experience,
                "dept": user.dept,
            },
        }
    ), 200


@app.delete("/api/admin/delete-user/<int:user_id>")
@jwt_required()
def delete_user_route(user_id):
    success, msg = delete_user(user_id)
    if success:
        return jsonify({"msg": msg}), 200
    else:
        return jsonify({"msg": msg}), 400


@app.put("/api/admin/block-user/<int:user_id>")
@jwt_required()
def block_user_route(user_id):
    success, msg = block_user(user_id)
    if success:
        return jsonify({"msg": msg}), 200
    else:
        return jsonify({"msg": msg}), 400


@app.get("/api/admin/patient/<int:patient_id>/history")
@jwt_required()
def get_patient_history_admin(patient_id):
    histories = (
        PatientHistory.query.filter_by(patient_id=patient_id)
        .order_by(PatientHistory.visit_date.desc())
        .all()
    )
    patient = User.query.get(patient_id)
    return jsonify(
        {
            "patient_name": patient.name if patient else "Patient",
            "history": [
                {
                    "id": h.id,
                    "visit_type": h.visit_type,
                    "tests_done": h.test_done,
                    "diagnosis": h.diagnosis,
                    "prescription": h.prescription,
                    "medicines": h.medicines,
                    "visit_date": h.visit_date.strftime("%Y-%m-%d %I:%M %p"),
                    "doctor_name": h.doctor.name if h.doctor else "Unknown",
                }
                for h in histories
            ],
        }
    ), 200
