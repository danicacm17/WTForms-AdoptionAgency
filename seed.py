from models import db, Pet
from app import app

# Drop all tables and recreate them
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create 5 sample pets
    pets = [
        Pet(name="Mittens", species="cat", photo_url="https://placekitten.com/200/300", age=3, notes="Loves to climb trees."),
        Pet(name="Rex", species="dog", photo_url="https://placedog.net/400/300", age=5, notes="Very friendly and playful."),
        Pet(name="Spike", species="porcupine", photo_url="https://placebear.com/200/300", age=2, notes="A little prickly but sweet."),
        Pet(name="Shadow", species="cat", photo_url="https://placekitten.com/250/350", age=1, notes="Prefers quiet environments."),
        Pet(name="Buddy", species="dog", photo_url="https://placedog.net/500/400", age=4, notes="Great with kids."),
    ]

    # Add and commit pets to the database
    db.session.add_all(pets)
    db.session.commit()

    print("Database seeded successfully!")
