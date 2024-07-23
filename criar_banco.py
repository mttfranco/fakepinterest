from FakePinterest import database, app
import FakePinterest.models

with app.app_context():
    database.create_all()
