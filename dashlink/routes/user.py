from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from dashlink import app, db
from dashlink.models import User, Url
from dashlink.forms import EditAccountForm

@app.route("/dashboard")
@login_required
def dashboard():
    dashed_url = Url.query.filter_by(user_id=current_user.id).all()
    user_pic = url_for('static', filename='img/profile_pic/' + current_user.img_file)
    return render_template("dashboard.html", title="dashboard", dashedURLs=dashed_url, img_file=user_pic)


# Edit user account

# Save profile picture
# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/img/profile_pic', picture_fn)
#     form_picture.save(picture_path)

#     return picture_fn

# The route
@app.route("/edit/profile", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditAccountForm()
    if form.validate_on_submit():

        # PROFILE PICTURES
        # if form.picture.data:
        #     picture_file = save_picture(form.picture.data)
        #     current_user.img_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your profile has been updated", 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static', filename='/img/profile_pic/' + current_user.img_file)

    return render_template("edit_account.html", title='Edit profile', form=form, img_file=img_file)
