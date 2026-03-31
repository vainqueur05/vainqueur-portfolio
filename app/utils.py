from app import db
from app.models import VisitLog
from flask import request

def log_visit(endpoint):
    visit = VisitLog(
        page=request.path,
        ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(visit)
    db.session.commit()