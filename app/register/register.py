from flask import Blueprint,render_template,redirect,url_for,flash
from app.forms import RegisterForm
from app.models import Employee
from app import db
register=Blueprint("app",__name__,static_folder="static",template_folder="templates")

@register.route("/register",methods=["POST","GET"])
def Register():
    form=RegisterForm()
    if form.validate_on_submit():
        employee_details = Employee(first_name=form.first_name.data,last_name=form.last_name.data,
                                    email=form.email.data,password=form.password.data,
                                    dob=form.dob.data,address=form.address.data,phone_number=form.phone_no.data)
        db.session.add(employee_details)
        db.session.commit()
        return redirect(url_for('app.Login'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template("register/register.html",form=form)
