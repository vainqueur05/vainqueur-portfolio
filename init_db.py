from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE contact_message ADD COLUMN read BOOLEAN DEFAULT 0"))
            conn.commit()
            print("Colonne 'read' ajoutée avec succès !")
        except Exception as e:
            print(f"Erreur : {e} (La colonne existe peut-être déjà)")

        try:
            # On en profite pour vérifier si WhatsAppClick doit être créée
            db.create_all()
            print("Vérification des autres tables terminée.")
        except Exception as e:
            print(f"Erreur lors du create_all : {e}")