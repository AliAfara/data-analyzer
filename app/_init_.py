from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, UserModel
from .routes import main

def create_app():
    # إنشاء التطبيق مع تحديد مكان مجلد القوالب
    app = Flask(__name__, template_folder="templates")  # هذا مهم

    # تحميل الإعدادات من ملف config.py
    app.config.from_pyfile('config.py')

    # تهيئة قاعدة البيانات
    db.init_app(app)

    # تهيئة LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    # تسجيل الـ blueprint
    app.register_blueprint(main)

    # التأكد من وجود المستخدم الافتراضي
    with app.app_context():
        db.create_all()
        if not UserModel.query.filter_by(username="testuser").first():
            from werkzeug.security import generate_password_hash
            user = UserModel(
                username="testuser",
                email="testuser@example.com",
                password=generate_password_hash("password123")
            )
            db.session.add(user)
            db.session.commit()

    return app
