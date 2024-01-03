from flask import render_template
from dashlink import app
from dashlink.forms import ContactForm

# The root
@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = ContactForm()
    return render_template("index.html", form=form)

@app.route("*", methods=['GET', 'POST'])
def not_found():
    return render_template("not_found.html", title="NOT Fount")