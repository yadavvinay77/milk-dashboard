from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils.forms import register_filters

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True,
                static_folder="../static", template_folder="../templates")

    # ✅ Load configuration
    try:
        app.config.from_object("config.Config")
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {e}")

    # ✅ Initialize extensions
    db.init_app(app)
    register_filters(app)

    # ✅ Create tables (Development only)
    with app.app_context():
        from . import models  # Main app models
        from blueprints.sweet_export import models as sweet_export_models
        db.create_all()

    # ✅ Register Blueprints
    from .routes.dashboard import dashboard_bp
    from .routes.logs import logs_bp
    from .routes.customers import customers_bp
    from .routes.reports import reports_bp
    from blueprints.sweet_export import sweet_export_bp

    app.register_blueprint(dashboard_bp)  # Root Dashboard
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(sweet_export_bp, url_prefix="/sweet_export")

    # ✅ Health check route
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app