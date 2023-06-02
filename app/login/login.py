from flask import Blueprint,render_template,redirect,url_for,flash
from app.forms import LoginForm
from app.models import Employee
from app import db
from flask_login import login_user
login_controller=Blueprint("app",__name__,static_folder="static",template_folder="templates")

@login_controller.route("/login",methods=['POST','GET'])
@login_controller.route("/",methods=['POST','GET'])
def Login():
    form=LoginForm()
    if form.validate_on_submit():
        attemped_email=Employee.query.filter_by(email=form.email.data).first()
        print("email ",attemped_email)
        if attemped_email and attemped_email.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attemped_email)
            flash(f'Success! You are logged in as: {attemped_email.email}', category='success')
            if form.email.data=="admin@xyz.com":
                return redirect(url_for('<admin>.Admin'))
            return redirect(url_for('<employee>.employee'))
        else:
            flash('Email and password are not match! Please try again', category='danger')
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template("login/login.html",form=form)