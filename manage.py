import os
from flask_migrate import Migrate, MigrateCommand

from app import app, db
import settings


app.config.from_object(settings)

migrate = Migrate(app, db)


if __name__ == '__main__':
    manager.run()
