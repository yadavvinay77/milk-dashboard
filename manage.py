from app import create_app, db
from flask_migrate import Migrate
from app.models import Customer, DailyLog  # registered for shell
from blueprints.sweet_export.models import SweetCustomer, SweetTransaction

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Customer": Customer,
        "DailyLog": DailyLog,
        "SweetCustomer": SweetCustomer,
        "SweetTransaction": SweetTransaction,
    }

if __name__ == "__main__":
    app.run()