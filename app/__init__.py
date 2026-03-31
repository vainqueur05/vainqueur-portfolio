from flask import Flask, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail, Message

# Initialisation globale
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # --- INTERCEPTEUR GLOBAL ---
    @app.before_request
    def handle_all_requests():
        # 1. Ignorer les fichiers statiques (images, css, js)
        if request.path.startswith('/static'):
            return None

        # 2. Ignorer l'admin et l'authentification
        if '/admin' in request.path or '/auth' in request.path:
            return None

        # 3. VERIFICATION MAINTENANCE
        from app.models import GlobalConfig
        maintenance_active = GlobalConfig.is_maintenance()
        
        # DEBUG CONSOLE (A supprimer après test)
        print(f"--- PATH: {request.path} | MAINT: {maintenance_active} ---")

        if maintenance_active:
            # Vérifier si l'utilisateur est admin
            is_admin = getattr(current_user, 'is_admin', False)
            if not (current_user.is_authenticated and is_admin):
                # On bloque et on affiche la page de maintenance
                return render_template('errors/maintenance.html'), 503

        # 4. LOG DES VISITES (Si pas en maintenance ou si admin)
        if request.endpoint and not request.endpoint.startswith('admin.'):
            try:
                from app.utils import log_visit as log_visit_util
                log_visit_util(request.endpoint)
            except Exception:
                pass # Ne pas faire planter le site si le log échoue

    # --- GESTION DES ERREURS ---
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app