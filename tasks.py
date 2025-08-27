from models import db, Website, StatusLog
import requests
from datetime import datetime

def check_websites(app):
    with app.app_context():
        websites = Website.query.all()
        for site in websites:
            try:
                response = requests.get(site.url, timeout=5)
                status = "UP" if response.status_code == 200 else "DOWN"
            except Exception:
                status = "DOWN"
            
            # Update website status and last_checked
            site.status = status
            site.last_checked = datetime.utcnow()
            
            # Optional: Add to status log for history
            log = StatusLog(website_id=site.id, status=status)
            db.session.add(log)
        
        db.session.commit()
        print(f"Checked {len(websites)} websites at {datetime.now()}")