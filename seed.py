import csv
from app import create_app, db, Episode, Guest, Appearance

app = create_app()  # Create an app instance

def seed_data():
    with app.app_context():  # Use the app context
        # Delete existing data
        try:
            db.session.query(Appearance).delete()
            db.session.query(Guest).delete()
            db.session.query(Episode).delete()
            db.session.commit()  # Commit the changes
            print("Existing data deleted successfully!")
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"Error occurred while deleting data: {e}")
            return

        # Create dictionaries to store episodes and guests for reference
        episodes = {}
        guests = {}
        
        # Read data from the seed CSV file
        with open('data/seed.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract the necessary fields from the row
                year = row['YEAR']
                occupation = row['GoogleKnowlege_Occupation']
                show = row['Show']  # Assuming this is the date now
                guest_names = row['Raw_Guest_List'].split(';')  # Assuming guests are separated by a semicolon

                # Generate a new episode number based on count
                episode_number = len(episodes) + 1

                # Seed Episodes
                episode = Episode(date=year, number=episode_number)  # Create the episode
                db.session.add(episode)
                episodes[episode_number] = episode  # Store episode for later reference

                # Commit to ensure the episode has an ID before proceeding
                db.session.commit()

                # Seed Guests
                for guest_name in guest_names:
                    guest_name = guest_name.strip()  # Remove any leading/trailing spaces
                    if guest_name not in guests:
                        guest = Guest(name=guest_name, occupation=occupation)
                        db.session.add(guest)
                        guests[guest_name] = guest  # Store guest for later reference

                # Seed Appearances
                for guest_name in guest_names:
                    guest_name = guest_name.strip()  # Remove any leading/trailing spaces
                    appearance = Appearance(
                        episode_id=episode.id,  # Use the latest episode ID
                        guest_id=guests[guest_name].id
                    )
                    db.session.add(appearance)

        # Commit the session after all data has been added
        try:
            db.session.commit()
            print("Data seeded successfully!")
        except Exception as e:
            db.session.rollback()  # Roll back the session in case of an error
            print(f"Error occurred while seeding data: {e}")

if __name__ == '__main__':
    seed_data()
