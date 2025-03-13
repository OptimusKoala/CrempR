from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import pyotp, qrcode, io, base64

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

SECRET_OTP = pyotp.random_base32()

@app.route('/login', methods=['GET', 'POST'])
def login():
    totp = pyotp.TOTP(SECRET_OTP)
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        otp = request.form.get('otp')
        if username == 'demo' and totp.verify(otp):
            user = User(username)
            login_user(user)
            return redirect(url_for('protected'))
        else:
            error = "Invalid username or OTP"

    qr_uri = totp.provisioning_uri("demo@client.com", issuer_name="POC Client")
    img = qrcode.make(qr_uri)
    buf = io.BytesIO()
    img.save(buf)
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    return render_template('login.html', qr_code=qr_b64, error=error)

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

@app.route('/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({"status": "authorized"}), 200
    else:
        return jsonify({"status": "unauthorized"}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')