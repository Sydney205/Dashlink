import secrets
from flask import render_template, url_for, request, redirect, abort, flash
from flask_login import current_user, login_required
from dashlink import app, db
from dashlink.forms import AddURLForm, EditURLForm
from dashlink.models import Url


# Dash New URL
@app.route("/url/new", methods=['GET', 'POST'])
@login_required
def new_url():
    form = AddURLForm()
    if form.validate_on_submit():
        short_code = secrets.token_hex(4)
        url = Url(title=form.title.data, long_url=form.long_url.data, short_url=short_code, desc=form.desc.data, owner=current_user)
        db.session.add(url)
        db.session.commit()

        flash("You dashed a URL", 'success')
        return redirect(url_for('dashboard'))
    return render_template("create_url.html", title='Shorten url', form=form)



# Redirect to the original link
@app.route('/<dashed_link>')
@login_required
def redirect_url(dashed_link):
    url_entry = Url.query.filter_by(user_id=current_user.id, short_url=dashed_link).first()

    if url_entry is not None:
       destination_url = url_entry.long_url

       return redirect(destination_url)
    return "Error: Dashed link not found"



# Edit links route
@app.route("/url/edit/<int:url_id>", methods=['GET', 'POST'])
@login_required
def edit_url(url_id):
    url = Url.query.get_or_404(url_id)

    if url.owner != current_user:
        # abort(403) # Forbidden
        return render_template("404link.html", title="Error link")
    
    form = EditURLForm()
    if form.validate_on_submit():
        url.title = form.title.data
        url.long_url = form.long_url.data
        url.short_url = form.short_url.data
        url.desc = form.desc.data
        db.session.commit()
        flash('Dashed Link has been updated', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.title.data = url.title
        form.long_url.data = url.long_url
        form.short_url.data = url.short_url
        form.desc.data = url.desc

    img_file = url_for('static', filename='/img/profile_pic/' + current_user.img_file)
        
    return render_template("edit_url.html", title='Edit link', form=form, url=url, img_file=img_file)



# Delete Link route
@app.route("/url/delete/<int:url_id>", methods=['POST'])
@login_required
def delete_url(url_id):
    url = Url.query.get_or_404(url_id) # not found

    if url.owner != current_user:
        # abort(403) # Forbidden
        return render_template("404link.html", title="Error link")

    db.session.delete(url)
    db.session.commit()
    flash('Your URL has been deleted', 'success')
    return redirect(url_for('dashboard'))
