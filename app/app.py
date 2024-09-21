from flask import Flask
from routes.course_route import course_bp
from routes.auth_route import auth_bp
from routes.user_route import user_bp
from service.mail_service import MailService
from config.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(course_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    mail_service = MailService(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
