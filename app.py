from flask import Flask
from routes.course_route import course_bp
from routes.auth_route import auth_bp
from routes.user_route import user_bp
from service.mail_service import MailService

app = Flask(__name__)
mail_service = MailService(app)

app.register_blueprint(course_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run(debug=True)
