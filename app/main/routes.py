from flask import render_template, redirect,request
from app.main import bp
from app.models import Bio, Service, Project, Testimonial, Skill, Stat, Benefit,WhatsAppClick

@bp.route('/')
def index():
    bio = Bio.get_singleton()
    services = Service.query.limit(3).all()
    projects = Project.query.limit(3).all()
    testimonials = Testimonial.query.limit(3).all()
    skills = Skill.query.all()
    stats = Stat.query.all()
    benefits = Benefit.query.all()
    return render_template('index.html',
                           bio=bio,
                           services=services,
                           projects=projects,
                           testimonials=testimonials,
                           skills=skills,
                           stats=stats,
                           benefits=benefits)

@bp.route('/about')
def about():
    bio = Bio.get_singleton()
    return render_template('about.html', bio=bio)

@bp.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@bp.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@bp.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@bp.route('/contact')
def contact():
    return render_template('contact.html')

from flask import redirect, request
from app import db  # Importe l'instance de la base de données
from app.models import WhatsAppClick  # Importe le modèle pour le tracking
@bp.route('/whatsapp-redirect')
def whatsapp_redirect():
    # Enregistrement du prospect dans la base de données
    try:
        new_click = WhatsAppClick(ip=request.remote_addr)
        db.session.add(new_click)
        db.session.commit()
    except Exception as e:
        # En cas d'erreur, on annule pour ne pas bloquer l'utilisateur
        db.session.rollback()
        print(f"Erreur tracking : {e}")

    # Redirection vers ton WhatsApp Business
    return redirect("https://wa.me/243895288981?text=Bonjour%20Vainqueur%2C%20je%20souhaite%20discuter%20d%27un%20projet")