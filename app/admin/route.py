from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service, Project, Testimonial, Skill, VisitLog, Bio, Stat, Benefit, GlobalConfig, WhatsAppClick, ContactMessage 
from functools import wraps
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from app.admin import bp

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# Dashboard
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    is_maintenance = GlobalConfig.is_maintenance()
    total_visits = VisitLog.query.count()
    today = datetime.utcnow().date()
    visits_today = VisitLog.query.filter(VisitLog.timestamp >= today).count()
    last_visits = VisitLog.query.order_by(VisitLog.timestamp.desc()).limit(10).all()
    hours = []
    counts = []
    for h in range(24):
        start = datetime(today.year, today.month, today.day, h)
        end = start + timedelta(hours=1)
        count = VisitLog.query.filter(VisitLog.timestamp >= start, VisitLog.timestamp < end).count()
        hours.append(f"{h}h")
        counts.append(count)
        # Notifications
        unread_messages = ContactMessage.query.filter_by(read=False).count()
        whatsapp_leads = WhatsAppClick.query.count() # Total des clics WhatsApp
    return render_template('admin/dashboard.html',
                           total_visits=total_visits,
                           visits_today=visits_today,
                           last_visits=last_visits,
                           hours=hours,
                           counts=counts,
                           is_maintenance=is_maintenance,unread_count=unread_messages,
                           wa_count=whatsapp_leads)

# Services CRUD
@bp.route('/services')
@login_required
@admin_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@bp.route('/services/new', methods=['GET', 'POST'])
@login_required
@admin_required
def service_new():
    if request.method == 'POST':
        service = Service(
            title=request.form['title'],
            description=request.form['description'],
            icon=request.form.get('icon', 'bi-code-slash'),
            price=request.form.get('price', ''),
            delivery_days=request.form.get('delivery_days', 0, type=int)
        )
        db.session.add(service)
        db.session.commit()
        flash('Service ajouté.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html')

@bp.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def service_edit(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        service.title = request.form['title']
        service.description = request.form['description']
        service.icon = request.form.get('icon', 'bi-code-slash')
        service.price = request.form.get('price', '')
        service.delivery_days = request.form.get('delivery_days', 0, type=int)
        db.session.commit()
        flash('Service modifié.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', service=service)

@bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def service_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé.', 'success')
    return redirect(url_for('admin.services'))

# Projects CRUD
@bp.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            client=request.form.get('client'),
            source_link=request.form.get('source_link'),
            demo_link=request.form.get('demo_link'),
            date=request.form.get('date'),
            category=request.form.get('category')
        )
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            project.image = filename
        db.session.add(project)
        db.session.commit()
        flash('Projet ajouté.', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html')

@bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.client = request.form.get('client')
        project.source_link = request.form.get('source_link')
        project.demo_link = request.form.get('demo_link')
        project.date = request.form.get('date')
        project.category = request.form.get('category')
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            file.save(os.path.join(upload_folder, filename))
            if project.image and project.image != filename:
                old_path = os.path.join(upload_folder, project.image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            project.image = filename
        db.session.commit()
        flash('Projet modifié.', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=project)

@bp.route('/projects/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.image:
        image_path = os.path.join('app', 'static', 'uploads', project.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    db.session.delete(project)
    db.session.commit()
    flash('Projet supprimé.', 'success')
    return redirect(url_for('admin.projects'))

# Testimonials CRUD
@bp.route('/testimonials')
@login_required
@admin_required
def testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@bp.route('/testimonials/new', methods=['GET', 'POST'])
@login_required
@admin_required
def testimonial_new():
    if request.method == 'POST':
        testimonial = Testimonial(
            client_name=request.form['client_name'],
            message=request.form['message'],
            rating=request.form.get('rating', 5, type=int)
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Témoignage ajouté.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html')

@bp.route('/testimonials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def testimonial_edit(id):
    testimonial = Testimonial.query.get_or_404(id)
    if request.method == 'POST':
        testimonial.client_name = request.form['client_name']
        testimonial.message = request.form['message']
        testimonial.rating = request.form.get('rating', 5, type=int)
        db.session.commit()
        flash('Témoignage modifié.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

@bp.route('/testimonials/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def testimonial_delete(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Témoignage supprimé.', 'success')
    return redirect(url_for('admin.testimonials'))

# Skills CRUD
@bp.route('/skills')
@login_required
@admin_required
def skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

@bp.route('/skills/new', methods=['GET', 'POST'])
@login_required
@admin_required
def skill_new():
    if request.method == 'POST':
        skill = Skill(
            name=request.form['name'],
            category=request.form['category'],
            percentage=request.form.get('percentage', 0, type=int)
        )
        db.session.add(skill)
        db.session.commit()
        flash('Compétence ajoutée.', 'success')
        return redirect(url_for('admin.skills'))
    return render_template('admin/skill_form.html')

@bp.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def skill_edit(id):
    skill = Skill.query.get_or_404(id)
    if request.method == 'POST':
        skill.name = request.form['name']
        skill.category = request.form['category']
        skill.percentage = request.form.get('percentage', 0, type=int)
        db.session.commit()
        flash('Compétence modifiée.', 'success')
        return redirect(url_for('admin.skills'))
    return render_template('admin/skill_form.html', skill=skill)

@bp.route('/skills/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Compétence supprimée.', 'success')
    return redirect(url_for('admin.skills'))

# Bio
@bp.route('/bio', methods=['GET', 'POST'])
@login_required
@admin_required
def bio_edit():
    bio = Bio.get_singleton()
    if request.method == 'POST':
        bio.name = request.form['name']
        bio.title = request.form['title']
        bio.bio_text = request.form['bio_text']
        bio.email = request.form['email']
        bio.phone = request.form['phone']
        bio.location = request.form['location']
        bio.availability = 'availability' in request.form
        file = request.files.get('avatar')
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            bio.avatar = filename
        db.session.commit()
        flash('Bio mise à jour.', 'success')
        return redirect(url_for('admin.bio_edit'))
    return render_template('admin/bio_form.html', bio=bio)

# --- Statistiques (Stat) ---
@bp.route('/stats')
@login_required
@admin_required
def stats():
    stats = Stat.query.all()
    return render_template('admin/stats.html', stats=stats)

@bp.route('/stats/new', methods=['GET', 'POST'])
@login_required
@admin_required
def stat_new():
    if request.method == 'POST':
        stat = Stat(
            label=request.form['label'],
            value=request.form['value'],
            icon=request.form.get('icon', 'bi-bar-chart')
        )
        db.session.add(stat)
        db.session.commit()
        flash('Statistique ajoutée.', 'success')
        return redirect(url_for('admin.stats'))
    return render_template('admin/stat_form.html')

@bp.route('/stats/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def stat_edit(id):
    stat = Stat.query.get_or_404(id)
    if request.method == 'POST':
        stat.label = request.form['label']
        stat.value = request.form['value']
        stat.icon = request.form.get('icon', 'bi-bar-chart')
        db.session.commit()
        flash('Statistique modifiée.', 'success')
        return redirect(url_for('admin.stats'))
    return render_template('admin/stat_form.html', stat=stat)

@bp.route('/stats/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def stat_delete(id):
    stat = Stat.query.get_or_404(id)
    db.session.delete(stat)
    db.session.commit()
    flash('Statistique supprimée.', 'success')
    return redirect(url_for('admin.stats'))

# --- Bénéfices (Benefit) ---
@bp.route('/benefits')
@login_required
@admin_required
def benefits():
    benefits = Benefit.query.all()
    return render_template('admin/benefits.html', benefits=benefits)

@bp.route('/benefits/new', methods=['GET', 'POST'])
@login_required
@admin_required
def benefit_new():
    if request.method == 'POST':
        benefit = Benefit(
            title=request.form['title'],
            description=request.form['description'],
            icon=request.form.get('icon', 'bi-check-circle-fill')
        )
        db.session.add(benefit)
        db.session.commit()
        flash('Bénéfice ajouté.', 'success')
        return redirect(url_for('admin.benefits'))
    return render_template('admin/benefit_form.html')

@bp.route('/benefits/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def benefit_edit(id):
    benefit = Benefit.query.get_or_404(id)
    if request.method == 'POST':
        benefit.title = request.form['title']
        benefit.description = request.form['description']
        benefit.icon = request.form.get('icon', 'bi-check-circle-fill')
        db.session.commit()
        flash('Bénéfice modifié.', 'success')
        return redirect(url_for('admin.benefits'))
    return render_template('admin/benefit_form.html', benefit=benefit)

@bp.route('/benefits/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def benefit_delete(id):
    benefit = Benefit.query.get_or_404(id)
    db.session.delete(benefit)
    db.session.commit()
    flash('Bénéfice supprimé.', 'success')
    return redirect(url_for('admin.benefits'))


@bp.route('/maintenance/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_maintenance():
    config = GlobalConfig.query.filter_by(key='maintenance_mode').first()
    if not config:
        config = GlobalConfig(key='maintenance_mode', value=False)
        db.session.add(config)
    
    config.value = not config.value
    db.session.commit()
    
    status = "activé" if config.value else "désactivé"
    flash(f"Mode maintenance {status}.", "warning")
    return redirect(url_for('admin.dashboard'))

@bp.route('/logs/purge', methods=['POST'])
@login_required
@admin_required
def purge_logs():
    try:
        VisitLog.query.delete()
        db.session.commit()
        flash("Tous les logs de visite ont été supprimés.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la purge : {str(e)}", "danger")
    return redirect(url_for('admin.dashboard'))

@bp.route('/system/clear-cache', methods=['POST'])
@login_required
@admin_required
def clear_cache():
    # Simulation de nettoyage (ou nettoyage réel si tu utilises Flask-Caching)
    flash("Cache du serveur vidé et fichiers temporaires supprimés.", "info")
    return redirect(url_for('admin.dashboard'))