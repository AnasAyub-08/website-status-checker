from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import routes
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from tasks import check_websites
from datetime import timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Session configuration - 30 minute timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "routes.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(routes)

# Initialize scheduler
scheduler = BackgroundScheduler()

# Pass the app instance to the check_websites function
scheduler.add_job(
    func=check_websites,
    trigger="interval",
    seconds=60,
    args=[app]  # Pass the app instance as argument
)

scheduler.start()

# Shut down the scheduler when exiting the app
import atexit
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)