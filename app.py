from flask_admin.contrib.sqla import ModelView
from data.__all_models import *
from blueprints import client
from flask import Flask, render_template, redirect, abort, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_admin import Admin
from data.db_session import app, db
import logging


@app.route("/")
def index():
    return "SGU API"


# for favicon
@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="img/favicon.ico"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/policy")
def policy():
    return render_template("policy.html", title="Политика конфиденциальности")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# register blueprint for mobile and desktop clients
app.register_blueprint(client.blueprint)

# add resources
# api.add_resource(ReceiptsListResource, "/api/v2/receipts")



if __name__ == "__main__":
    admin = Admin(app, name='Admin', template_mode='bootstrap3', url='/admin')

    db.create_all()
    db.session.commit()

    admin.add_view(ModelView(user.User, db.session))
    admin.add_view(ModelView(enrollee.Enrollee, db.session))

    app.secret_key = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

