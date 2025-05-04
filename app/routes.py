from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash  # تأكد من استيراد generate_password_hash
from .models import UserModel, db
from .forms import LoginForm, RegistrationForm

# تعريف الـ Blueprint
main = Blueprint('main', __name__)

# الصفحة الرئيسية
@main.route('/')
def index():
    return render_template('index.html')

# صفحة تسجيل الدخول
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')

    return render_template('login.html', form=form)

# صفحة التسجيل
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # التأكد إذا كان اسم المستخدم أو البريد الإلكتروني موجود
        existing_user = UserModel.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('اسم المستخدم موجود مسبقاً', 'danger')
            return redirect(url_for('main.register'))

        existing_email = UserModel.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('البريد الإلكتروني موجود مسبقاً', 'danger')
            return redirect(url_for('main.register'))

        # تشفير كلمة المرور
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = UserModel(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# صفحة الملف الشخصي (محمية للمستخدمين المسجلين)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# تسجيل الخروج
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('main.index'))
