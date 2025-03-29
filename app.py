from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import random
import time
import os
import paramiko

def ssh_connect():
    host = '103.244.145.77'  # استبدل هنا بـ IP الخاص بالخادم
    username = 'kali_eslam'  # استبدل هنا باسم المستخدم الخاص بك
    password = 'kali_eslam'  # استبدل هنا بكلمة المرور الخاصة بك
    port = 22  # عادة ما يكون البورت الافتراضي لـ SSH هو 22

    # إنشاء الاتصال عبر SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)

    # تنفيذ أوامر عبر SSH (على سبيل المثال طباعة الـ hostname)
    stdin, stdout, stderr = client.exec_command('hostname')
    print(stdout.read().decode())

    client.close()















app = Flask(__name__)
app.secret_key = 'your_secret_key'

# إعدادات قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعدادات البريد الإلكتروني
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alajmiaslam@gmail.com'
app.config['MAIL_PASSWORD'] = 'mnbvcxz890*/#'
mail = Mail(app)
db = SQLAlchemy(app)

# نموذج المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(100), nullable=True)
    token_expiry = db.Column(db.Float, nullable=True)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        # التحقق من وجود البريد في قاعدة البيانات
        user = User.query.filter_by(email=email).first()
        if user:
            # توليد رمز التحقق وإرساله بالبريد الإلكتروني
            token = generate_token()
            user.token = token
            user.token_expiry = time.time() + 60  # صلاحية الرمز 60 ثانية
            db.session.commit()
            
            send_verification_email(user.email, token)
            flash('تم إرسال رمز التحقق إلى بريدك الإلكتروني!')
            return redirect(url_for('verify'))
        else:
            flash('البريد الإلكتروني غير موجود في قاعدة البيانات')
    
    return render_template('login.html')

# صفحة التحقق من الرمز
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        token = request.form['token']
        email = request.form['email']
        
        # التحقق من الرمز المدخل
        user = User.query.filter_by(email=email).first()
        if user and user.token == token and time.time() < user.token_expiry:
            flash('تم التحقق بنجاح!')
            return redirect(url_for('upload'))
        else:
            flash('الرمز غير صحيح أو انتهت صلاحيته!')
    
    return render_template('verify.html')

# صفحة رفع الملفات
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join('uploads', filename))
            flash(f'تم رفع الملف {filename} بنجاح!')
            return redirect(url_for('upload'))
    return render_template('upload.html')

# توليد رمز تحقق عشوائي
def generate_token():
    return str(random.randint(100000, 999999))

# إرسال البريد الإلكتروني
def send_verification_email(email, token):
    msg = Message('رمز التحقق', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'رمز التحقق الخاص بك هو: {token}'
    mail.send(msg)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
    
    
    
    
    
    
    
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# إعدادات البريد الإلكتروني
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alaseepee@gmail.com'  # استبدلها ببريدك الإلكتروني
app.config['MAIL_PASSWORD'] = 'mnbvcxz890*/#'  # استبدلها بكلمة مرور بريدك الإلكتروني
mail = Mail(app)

# صفحة رفع الملفات
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))  # تحديد مكان حفظ الملف
            flash(f'تم رفع الملف {filename} بنجاح!')
            return redirect(url_for('upload'))
    return render_template('upload.html')  # تأكد من وجود ملف HTML لواجهة رفع الملفات

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    @app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        user = 'admin'  # أو استبدل هذه القيمة بناءً على بيانات المستخدم الذي تم التحقق منه
        
        if user == 'admin':
            # الصلاحيات المرتفعة، يمكن رفع أنواع ملفات إضافية
            ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe'}
        else:
            # صلاحيات منخفضة، يمكن رفع أنواع معينة فقط
            ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            flash(f'تم رفع الملف {filename} بنجاح!')
            return redirect(url_for('upload'))
    return render_template('upload.html')

# دالة التحقق من نوع الملف
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions