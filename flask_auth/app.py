from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp, qrcode, io, base64, os, time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Config SQLAlchemy avec MySQL (MariaDB)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    SESSION_COOKIE_DOMAIN=".crempr.fr",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False
)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # nom explicite de la table existante
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.Enum('user', 'admin'), default='user')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('protected'))

    error = None
    secret_otp = os.getenv('SECRET_OTP')
    totp = pyotp.TOTP(secret_otp)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if totp.verify(otp):
                login_user(user)
                return redirect(url_for('protected'))
            else:
                error = "OTP incorrect."
        else:
            error = "Identifiants invalides."

    qr_uri = totp.provisioning_uri("demo@crempr.fr", issuer_name="CrempR Auth")
    img = qrcode.make(qr_uri)
    buf = io.BytesIO()
    img.save(buf)
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    return render_template('login.html', qr_code=qr_b64, error=error)

@app.route('/protected')
@login_required
def protected():
    is_admin = current_user.role == 'admin'
    return render_template('protected.html', admin=is_admin, username=current_user.username)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')
        if User.query.filter_by(username=username).first():
            error = "Utilisateur existe déjà."
        else:
            hashed_pwd = generate_password_hash(password)
            user = User(username=username, password=hashed_pwd, role=role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('inscription.html', error=error)

@app.route('/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({"status": "authorized"}), 200
    else:
        return jsonify({"status": "unauthorized"}), 401

@app.route('/protected')
@login_required
def protected_page():
    return render_template('protected.html', admin=(current_user.role == 'admin'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)