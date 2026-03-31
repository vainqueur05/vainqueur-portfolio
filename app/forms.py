from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

# ... (imports existants)

class ProjectForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description')
    image = FileField('Image')
    link = StringField('Lien')
    demo_link = StringField('Lien de démo')
    code_link = StringField('Lien du code')
    client = StringField('Client')
    date = StringField('Date (YYYY)')
    submit = SubmitField('Enregistrer')

class ServiceForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description')
    icon = StringField('Icône Bootstrap')
    price = StringField('Prix indicatif')
    delivery_time = StringField('Délai de livraison')
    featured = BooleanField('Mis en avant')
    submit = SubmitField('Enregistrer')

class TestimonialForm(FlaskForm):
    author = StringField('Auteur', validators=[DataRequired()])
    content = TextAreaField('Témoignage', validators=[DataRequired()])
    role = StringField('Rôle / Fonction')
    avatar = FileField('Avatar')
    rating = IntegerField('Note (1-5)')
    submit = SubmitField('Enregistrer')

class SkillForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    category = StringField('Catégorie (frontend, backend, tools, ai)')
    level = IntegerField('Niveau (%)')
    icon = StringField('Icône Bootstrap')
    submit = SubmitField('Enregistrer')

class BioForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    title = StringField('Titre', validators=[DataRequired()])
    bio = TextAreaField('Biographie')
    location = StringField('Localisation')
    email = StringField('Email', validators=[Email()])
    available = BooleanField('Disponible')
    avatar = FileField('Photo de profil')
    submit = SubmitField('Enregistrer')