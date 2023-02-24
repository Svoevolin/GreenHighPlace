from flask_migrate import Migrate
from app.config.config import app, db

from app.models.CustomerModel import Customer

migrate = Migrate(app, db)

app.app_context().push()
