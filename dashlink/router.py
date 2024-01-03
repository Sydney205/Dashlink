# # import os
# import secrets
# import uuid
# from dashlink import app, db, bcrypt
# from flask import render_template, url_for, flash, redirect, request, abort
# from dashlink.forms import ContactForm, SignupForm, LoginForm, EditAccountForm, AddURLForm, EditURLForm
# from dashlink.models import User, Url
# from flask_login import login_user, current_user, logout_user, login_required

# # Home route
# @app.route("/", methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])
# def home():
#     form = ContactForm()    
#     return render_template("index.html", form=form)


# # Signup route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()

#     # Check if user is logged in
#     if current_user.is_authenticated:
#         flash("You are logged in", "success")
#         return redirect(url_for('home'))

#     if form.validate_on_submit():
#         try:
#             # Check if the username already exists in the database
#             existing_user = User.query.filter_by(username=form.username.data).first()
#             if existing_user:
#                 flash('Username already exists. Please choose a different username.', 'error')
#                 return redirect(url_for('auth.signup'))

#             # Hash the password and create user's account
#             hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#             user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
#             db.session.add(user)
#             db.session.commit()

#             flash(f"Thanks for signing up {form.username.data}", 'success')
#             return redirect(url_for('dashboard'))
#         except Exception as e:
#             db.session.rollback()
#             flash('An error occurred while processing your request.', 'error')
#             print(f"Error: {e}")
#     return render_template('signup.html', title='Signup', form=form)



# # Login route
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     # Check if user is logged in
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
    
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user)
#             next_page = request.args.get('next') # If the next page exists, next is going to be equal to the next parameters, else it's going to be none
#             flash("You are logged in", 'success')
#             return redirect(next_page) if next_page else redirect(url_for('dashboard'))
#         else:
#             flash("Incorrect email or password", 'error')

#     return render_template("login.html", title='Login', form=form)


# # Logout route
# @app.route('/logout')
# @login_required
# def logout():
#     if current_user.is_authenticated:
#         logout_user()
#         flash('You have been logged out.', 'success')
#     else:
#         flash('You are not logged in.', 'error')

#     return redirect(url_for('home'))



# # Dashboard route
# @app.route("/dashboard", methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     user_url = Url.query.filter_by(user_id=current_user.id).all()
#     img_file = url_for('static', filename='/img/profile_pic/' + current_user.img_file)
#     return render_template("dashboard.html", title='Dashboard', dashedURLs=user_url, img_file=img_file)



# # Edit user account

# # Save profile picture
# # def save_picture(form_picture):
# #     random_hex = secrets.token_hex(8)
# #     _, f_ext = os.path.splitext(form_picture.filename)
# #     picture_fn = random_hex + f_ext
# #     picture_path = os.path.join(app.root_path, 'static/img/profile_pic', picture_fn)
# #     form_picture.save(picture_path)

# #     return picture_fn

# # The route
# @app.route("/edit/profile", methods=['GET', 'POST'])
# @login_required
# def edit_account():
#     form = EditAccountForm()
#     if form.validate_on_submit():

#         # PROFILE PICTURES
#         # if form.picture.data:
#         #     picture_file = save_picture(form.picture.data)
#         #     current_user.img_file = picture_file

#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash("Your profile has been updated", 'success')
#         return redirect(url_for('dashboard'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email

#     img_file = url_for('static', filename='/img/profile_pic/' + current_user.img_file)

#     return render_template("edit_account.html", title='Edit profile', form=form, img_file=img_file)



# # Dash New URL
# @app.route("/url/new", methods=['GET', 'POST'])
# @login_required
# def new_url():
#     form = AddURLForm()
#     if form.validate_on_submit():
#         short_code = secrets.token_hex(4)
#         url = Url(title=form.title.data, long_url=form.long_url.data, short_url=short_code, desc=form.desc.data, owner=current_user)
#         db.session.add(url)
#         db.session.commit()

#         flash("You dashed a URL", 'success')
#         return redirect(url_for('dashboard'))
#     return render_template("create_url.html", title='Shorten url', form=form)



# # Redirect to the original link
# @app.route('/<dashed_link>')
# @login_required
# def redirect_url(dashed_link):
#     url_entry = Url.query.filter_by(user_id=current_user.id, short_url=dashed_link).first()

#     if url_entry is not None:
#        destination_url = url_entry.long_url

#        return redirect(destination_url)
#     return "Error: Dashed link not found"



# # Edit links route
# @app.route("/url/edit/<int:url_id>", methods=['GET', 'POST'])
# @login_required
# def edit_url(url_id):
#     url = Url.query.get_or_404(url_id)

#     if url.owner != current_user:
#         abort(403) # Forbidden
    
#     form = EditURLForm()
#     if form.validate_on_submit():
#         url.title = form.title.data
#         url.long_url = form.long_url.data
#         url.short_url = form.short_url.data
#         url.desc = form.desc.data
#         db.session.commit()
#         flash('Dashed Link has been updated', 'success')
#         return redirect(url_for('dashboard'))
#     elif request.method == 'GET':
#         form.title.data = url.title
#         form.long_url.data = url.long_url
#         form.short_url.data = url.short_url
#         form.desc.data = url.desc

#     img_file = url_for('static', filename='/img/profile_pic/' + current_user.img_file)
        
#     return render_template("edit_url.html", title='Edit link', form=form, url=url, img_file=img_file)



# # Delete Link route
# @app.route("/url/delete/<int:url_id>", methods=['POST'])
# @login_required
# def delete_url(url_id):
#     url = Url.query.get_or_404(url_id) # not found

#     if url.owner != current_user:
#         abort(403) # Forbidden
#     db.session.delete(url)
#     db.session.commit()
#     flash('Your URL has been deleted', 'success')
#     return redirect(url_for('dashboard'))
