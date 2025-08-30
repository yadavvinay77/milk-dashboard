from flask import Blueprint

sweet_export_bp = Blueprint(
    "sweet_export_bp",
    __name__,
    template_folder="../../templates/sweet_export"
)

from . import routes