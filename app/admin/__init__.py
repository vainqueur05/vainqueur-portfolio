from flask import Blueprint

# On définit le Blueprint ICI et UNE SEULE FOIS
bp = Blueprint('admin', __name__)

# On importe les routes à la fin pour que 'bp' existe déjà quand 'route.py' est lu
from app.admin import route