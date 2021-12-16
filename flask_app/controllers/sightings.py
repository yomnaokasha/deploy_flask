from flask_app import app
from flask import flash
from flask import render_template, session, redirect, request
from flask_app.models import user, sighting


@app.route("/new/sighting")
def add():
    data = {
        "id": session["user_id"]
    }
    return render_template("new_sighting.html", logged_user=user.User.get_user_id(data))


@app.route("/create/sighting", methods=["POST"])
def create_sighting():
    if not sighting.Sighting.validate_sighting(request.form):
        return redirect("/new/sighting")
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date": request.form["date"],
        "num_sasquatch": request.form["num_sasquatch"],
        "user_id": session["user_id"],
    }
    sighting.Sighting.add(data)
    return redirect("/dashboard")


@app.route("/edit/<int:id>")
def edit_sighting(id):

    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("edit.html", sighting=sighting.Sighting.get_one(data), logged_user=user.User.get_user_id(user_data))


@app.route("/update/sighting", methods=["POST"])
def update_sighting():
    if "user_id" not in session:
        return redirect("/logout")
    if not sighting.Sighting.validate_sighting(request.form):
        return redirect("/new/sighting")
    data = {
        "id": request.form["id"],
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date": request.form["date"],
        "num_sasquatch": request.form["num_sasquatch"],
        "user_id": session["user_id"],

    }
    sighting.Sighting.update_info(data)
    return redirect("/dashboard")


@app.route("/show/<int:id>")
def show_sighting(id):
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    logged_user = user.User.get_user_id(user_data)
    this_sighting = sighting.Sighting.get_one_with_skeptics(data)
    is_skeptic = False
    for skeptic in this_sighting.skeptics:
        if skeptic.id == session["user_id"]:
            is_skeptic = True
    return render_template("show.html", sighting=this_sighting, logged_user=logged_user, is_skeptic=is_skeptic)


@app.route("/destroy/<int:id>")
def destroy_sighting(id):
    data = {
        "id": id
    }
    sighting.Sighting.delete(data)
    return redirect("/dashboard")


@app.route("/skeptic/add", methods=["POST"])
def add_skeptic():
    sighting_id = request.form['sighting_id']
    data = {
        "user_id": session["user_id"],
        "sighting_id": sighting_id,
    }
    sighting.Sighting.add_skeptic(data)
    return redirect(f"/show/{sighting_id}")


@app.route("/skeptic/delete", methods=["POST"])
def delete_skeptic():
    sighting_id = request.form['sighting_id']
    data = {
        "user_id": session["user_id"],
        "sighting_id": sighting_id,
    }
    sighting.Sighting.delete_skeptic(data)
    return redirect(f"/show/{sighting_id}")
