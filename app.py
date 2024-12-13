from flask import Flask, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "430-875-209"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# Wrap the db.create_all() call within the application context
with app.app_context():
    db.create_all()

toolbar = DebugToolbarExtension(app)


##############################################################################


@app.route("/")
def list_pets():
    """List all pets."""

    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a pet."""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect("/") 

    else:
        return render_template("pet_add_form.html", form=form)


@app.route("/<int:pet_id>/edit", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data  # This will reflect True or False based on checkbox
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect("/")

    return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)

@app.route("/<int:pet_id>/delete", methods=["POST"])
def delete_pet(pet_id):
    """Delete a pet."""
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()  # Ensure that the pet is actually deleted
    flash(f"{pet.name} has been deleted.")
    return redirect("/")  # Redirect back to the homepage after deletion