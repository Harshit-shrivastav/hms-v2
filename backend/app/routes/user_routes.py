
from flask import jsonify, request, make_response
from app import flask_app as app, db, cache
from flask_jwt_extended import jwt_required, create_access_token, unset_jwt_cookies, set_access_cookies, get_jwt_identity
from datetime import timedelta
from app.models.models import User, Appointment, PatientHistory
from werkzeug.security import check_password_hash, generate_password_hash
import os


@app.route('/api')
def index():
    return jsonify({'running': True}), 200

@app.route('/api')
@app.get('/api/')
def api_root():
    return jsonify({'running': True}), 200

@app.post('/api/dashboard')
def dashboard():
    return jsonify({'message': 'dashboard!'})


@app.post('/api/register')
def register():
    data = request.get_json()

    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    name = data.get('name', '').strip()
    gender = data.get('gender', '').strip()
    age = data.get('age')

    if not all([username, email, password, confirm_password, name, gender]):
        return jsonify({"msg": "All fields are required."}), 400

    if age:
        try:
            age = int(age)
        except ValueError:
            return jsonify({"msg": "Age must be a valid number."}), 400
    else:
        return jsonify({"msg": "Age is required."}), 400

    if password != confirm_password:
        return jsonify({"msg": "Passwords do not match."}), 400

    if len(password) < 5:
        return jsonify({"msg": "Password should be at least 5 characters."}), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({"msg": "Username or email already registered."}), 409

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        name=name,
        gender=gender,
        role='patient',
        age=age
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error occurred.", "error": str(e)}), 500

    access_token = create_access_token(
        identity=str(new_user.id),
        additional_claims={"role": new_user.role, "email": new_user.email}
    )

    response = make_response(jsonify({
        "msg": "Registration successful",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "name": new_user.name,
            "role": new_user.role,
            "email": new_user.email
        }
    }), 201)

    set_access_cookies(response, access_token)
    return response


@app.post('/api/login')
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"msg": "Email and password are required."}), 400

    if len(password) < 5:
        return jsonify({"msg": "Password must be at least 5 characters."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid email or password."}), 401

    if user.role.startswith('BLOCKED_'):
        return jsonify({"msg": "Your account has been blocked. Please contact admin."}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "email": user.email,
            "username": user.username
        }
    )

    response = make_response(jsonify({
        "msg": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "role": user.role,
            "email": user.email
        }
    }), 200)

    set_access_cookies(response, access_token)

    return response

@app.post("/api/logout")
def logout():
    response = make_response(jsonify({"message": "Logged out!"}))
    unset_jwt_cookies(response)
    return response, 200

@app.get("/api/login-status")
@jwt_required(optional=True)
def get_login():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"logged_in": False, "msg": "Not authenticated"}), 401
    user = User.query.get(current_user_id)
    return jsonify({
        "logged_in": True,
        "user_id": current_user_id,
        "user": {
            "id": user.id,
            "role": user.role if user else ''
        }
    }), 200


@app.get("/api/patient/profile")
@jwt_required()
def get_patient():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found."}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "gender": user.gender,
        "age": user.age,
        "experience": user.experience,
        "dept": user.dept
    })


@app.put("/api/patient/profile")
@jwt_required()
def update_patient():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided."}), 400

    if 'name' in data:
        user.name = data['name']

    if 'email' in data:
        existing_user = User.query.filter(
            User.email == data['email'],
            User.id != current_user_id
        ).first()
        if existing_user:
            return jsonify({"msg": "Email already in use."}), 400
        user.email = data['email']

    if 'gender' in data:
        user.gender = data['gender']

    if 'age' in data:
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                return jsonify({"msg": "Age must be between 0 and 150."}), 400
            user.age = age
        except (ValueError, TypeError):
            return jsonify({"msg": "Age must be a valid number."}), 400

    if 'experience' in data:
        user.experience = data['experience']

    if 'dept' in data:
        user.dept = data['dept']

    db.session.commit()

    return jsonify({
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
            "dept": user.dept
        }
    }), 200


@app.get("/api/doctors/<int:doctor_id>")
@jwt_required()
def get_doctor(doctor_id):
    doc = User.query.filter_by(id=doctor_id, role='doctor').first()
    if not doc:
        return jsonify({"msg": "Doctor not found."}), 404
    return jsonify({
        "id": doc.id,
        "name": doc.name,
        "experience": doc.experience,
        "dept": doc.dept
    }), 200

@app.post('/api/cancel-appointment')
@jwt_required()
def cancel_appointment():
    data = request.get_json()
    appointment_id = data.get('appointment_id')
    
    if not appointment_id:
        return jsonify({"msg": "Appointment ID is required."}), 400
    
    current_user_id = get_jwt_identity()
    
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        patient_id=current_user_id,
        status='booked'
    ).first()
    
    if not appointment:
        return jsonify({"msg": "Appointment not found or already cancelled."}), 404
    
    try:
        appointment.status = 'cancelled'
        db.session.commit()
        return jsonify({'msg': 'Appointment cancelled successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@app.get('/api/appointments')
@jwt_required()
def get_appointments():
    current_user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(patient_id=current_user_id).all()
    return jsonify({'data': [{
        'id': apt.id,
        'patient_id': apt.patient_id,
        'date': apt.date.isoformat(),
        'doc_name': apt.doc_name,
        'doc_dept': apt.doc_dept,
        'time_slot': apt.time_slot,
        'status': apt.status
    } for apt in appointments]}), 200


@app.post('/api/patient/export')
@jwt_required()
def export_patient_data():
    from app.tasks import send_patient_export_email
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user and user.email:
        send_patient_export_email.delay(user.email, user.name, current_user_id)
        return jsonify({'msg': 'Export email sent'}), 200
    return jsonify({'msg': 'No email found'}), 400


@app.get('/api/patient/export-csv')
def download_patient_csv():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'msg': 'Invalid link'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    histories = PatientHistory.query.filter_by(patient_id=user_id).all()
    appointments = Appointment.query.filter_by(patient_id=user_id).all()

    csv = "User ID,Username,Patient Name,Email,Doctor,Department,Date,Status\n"
    for apt in appointments:
        csv += f"{user.id},{user.username},{user.name},{user.email},{apt.doc_name},{apt.doc_dept},{apt.date.isoformat()},{apt.status}\n"

    for h in histories:
        csv += f"{user.id},{user.username},{user.name},{user.email},{h.diagnosis or '-'},{h.test_done or '-'},{h.visit_date.strftime('%Y-%m-%d')},-\n"

    response = make_response(csv)
    response.headers['Content-Disposition'] = f'attachment;filename=patient_report_{user.username}.csv'
    return response

