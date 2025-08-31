from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Website
from flask import jsonify
from datetime import datetime

routes = Blueprint("routes", __name__)

@routes.route("/")
def root():
    # Redirect to login page for fresh visitors
    if not current_user.is_authenticated:
        return redirect(url_for("routes.login"))
    # If already logged in, go to dashboard
    return redirect(url_for("routes.dashboard"))

@routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))
        
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("routes.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("routes.login"))
    return render_template("register.html")

@routes.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))
        
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("routes.dashboard"))
        flash("Login failed. Check email & password.", "danger")
    return render_template("login.html")

@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.login"))

@routes.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        url = request.form["url"].strip()

        # Avoid duplicates for the same user
        existing = Website.query.filter_by(user_id=current_user.id, url=url).first()
        if existing:
            flash("This website is already added!", "warning")
        else:
            new_site = Website(url=url, owner=current_user)
            db.session.add(new_site)
            db.session.commit()
            flash("Website added!", "success")

        # 🔹 Redirect so refresh won't re-submit the form
        return redirect(url_for("routes.dashboard"))

    # GET request
    websites = Website.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", websites=websites, now=datetime.now())

@routes.route("/delete_website/<int:website_id>", methods=["POST"])
@login_required
def delete_website(website_id):
    site = Website.query.get_or_404(website_id)

    # Ensure only the owner can delete
    if site.owner != current_user:
        flash("You are not authorized to delete this website.", "danger")
        return redirect(url_for("routes.dashboard"))

    db.session.delete(site)
    db.session.commit()
    flash("Website deleted!", "success")
    return redirect(url_for("routes.dashboard"))

@routes.route('/api/statuses')
@login_required
def api_statuses():
    websites = Website.query.filter_by(user_id=current_user.id).all()
    statuses = []
    for site in websites:
        statuses.append({
            'id': site.id,
            'status': site.status,
            'last_checked': site.last_checked.strftime('%Y-%m-%d %H:%M:%S') if site.last_checked else None
        })
    return jsonify({'statuses': statuses})