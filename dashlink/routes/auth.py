from flask import render_template, url_for, request, redirect, flash
from dashlink import app, db, bcrypt
from dashlink.models import User
from flask_login import current_user, login_user, login_required, logout_user
from dashlink.forms import SignupForm, LoginForm
from dashlink.routes.user import dashboard

# The signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Redirect to dashboard if already authenticated
    if current_user.is_authenticated:
        flash("You're still logged in", "info")
        return redirect(url_for("dashboard"))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(username=form.username.data, email=form.username.data).first()
        if existing_user:
            flash("User already exists", "error")
            return render_template("signup.html")
        
        # Hash password and create User
        hashed_pwd = bcrypt.generate_password_hash(form.password.data, 10).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()

        flash(f"Thanks for signing up {form.username.data}", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("signup.html", title="signup", form=form)



# The login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirect to dashboard if already authenticated
    if current_user.is_authenticated:
        flash("You're still logged in", "info")
        return render_template(url_for("dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # If the next page exists, next is going to be equal to the next parameters, else it's going to be none
            next_page = request.args.get('next')
            flash(f"Welcome {current_user.username}", 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash("Incorrect email or password", 'error')

    return render_template("login.html", title="login", form=form)



# Logout route
@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out.', 'success')
    else:
        flash('You are not logged in.', 'error')

    return redirect(url_for('home'))
