from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
from flask_app.models import user


class Sighting:
    def __init__(self, data):
        self.id = data["id"]
        self.location = data["location"]
        self.what_happened = data["what_happened"]
        self.date = data["date"]
        self.num_sasquatch = data["num_sasquatch"]
        self.user_id = data["user_id"]
        self.user = None
        self.skeptics = []
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def add(cls, data):
        query = "INSERT INTO sightings (location, what_happened, date,num_sasquatch,user_id) VALUES (%(location)s, %(what_happened)s, %(date)s,%(num_sasquatch)s, %(user_id)s);"
        connectToMySQL("sighting_schema").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL("sighting_schema").query_db(query)
        all_sightings = []
        for row in results:
            data = {
                "id": row["id"]
            }
            all_sightings.append(Sighting.get_one_with_skeptics(data))
        return all_sightings

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL("sighting_schema").query_db(query, data)
        this_sighting = cls(results[0])
        user_info = {
            "id": results[0]["user_id"]
        }
        this_user = user.User.get_user_id(user_info)
        this_sighting.user = this_user
        return this_sighting

    @classmethod
    def get_one_with_skeptics(cls, data):
        query = "select * from sightings left join skeptics on sightings.id = skeptics.sighting_id left join users on users.id = skeptics.user_id where sightings.id = %(id)s"
        results = connectToMySQL("sighting_schema").query_db(query, data)

        this_sighting = cls(results[0])
        user_info = {
            "id": results[0]["user_id"]
        }
        this_user = user.User.get_user_id(user_info)
        this_sighting.user = this_user
        for row in results:
            if row['users.id'] != None:
                skeptic_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }
                this_sighting.skeptics.append(user.User(skeptic_data))
        return this_sighting

    @classmethod
    def update_info(cls, data):
        query = "update sightings  set location = %(location)s, what_happened=%(what_happened)s, date=%(date)s,num_sasquatch=%(num_sasquatch)s ,updated_at = Now() where id = %(id)s;"
        return connectToMySQL("sighting_schema").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "Delete FROM sightings where id = %(id)s;"
        return connectToMySQL("sighting_schema").query_db(query, data)

    @classmethod
    def add_skeptic(cls, data):
        query = "INSERT INTO skeptics (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        return connectToMySQL("sighting_schema").query_db(query, data)

    @classmethod
    def delete_skeptic(cls, data):
        query = "DELETE FROM skeptics WHERE (user_id= %(user_id)s) and (sighting_id = %(sighting_id)s);"
        return connectToMySQL("sighting_schema").query_db(query, data)

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data["location"]) == 0:
            flash("location is required.")
            is_valid = False
        if len(data["what_happened"]) == 0:
            flash(" what_happened is required.")
            is_valid = False
        if len(data["date"]) == "":
            flash(" date is required.")
            is_valid = False
        if len(data["num_sasquatch"]) == 0:
            flash(" number of sasquatch must be one or more.")
            is_valid = False
        return is_valid
