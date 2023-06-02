from app import app,api
from app.register.register import register
from app.login.login import login_controller
from app.employee_detail.employee_detail import employee_detail
from app.admin.admin import admin,Search
from flask_login import logout_user
from flask import render_template,flash,redirect,url_for
from app.models import Employee
app.register_blueprint(login_controller,url_for="/login")
app.register_blueprint(register,name="<register>",url_for="/register")
app.register_blueprint(employee_detail,name="<employee>",url_for="/employee_detail")
app.register_blueprint(admin,name="<admin>",url_for="/admin")
api.add_resource(Search, '/search/<string:search_value>')

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("app.Login"))