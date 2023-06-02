from flask import Blueprint,render_template,redirect,url_for,flash
from app.forms import RegisterForm
from app.models import Employee
from app import db
from flask_login import login_required,current_user
from datetime import datetime, date

employee_detail=Blueprint("app",__name__,static_folder="static",template_folder="templates")

@employee_detail.route("/employee_detail",methods=['POST','GET'])
@login_required
def employee():
    return render_template('employee_detail/employee.html')

@employee_detail.route("/employee_detail_update",methods=['POST','GET'])
@login_required
def employee_update():
    form=RegisterForm()
    if form.validate_on_submit():
        update_check(form)
    else:
        form.first_name.data=current_user.first_name
        form.last_name.data=current_user.last_name
        form.email.data=current_user.email
        form.phone_no.data=current_user.phone_number
        cr_date =current_user.dob.split('-')
        form.dob.data=date(int(cr_date[0]),int(cr_date[1]),int(cr_date[2]))
        form.address.data=current_user.address
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template('employee_detail/update_details.html',form=form)

def update_check(form):
    attemped_id=Employee.query.filter_by(id=current_user.id).first()
    if attemped_id and attemped_id.check_password_correction(
                attempted_password=form.password.data):
        print("password check")
        updated_value(form,attemped_id)
    else:
        flash('Email and password are not match! Please try again', category='danger')
def updated_value(form,attemped_id):
    attemped_id.first_name=form.first_name.data
    attemped_id.last_name=form.last_name.data
    attemped_id.password=form.password.data
    attemped_id.dob=form.dob.data
    attemped_id.address=form.address.data
    attemped_id.phone_number=form.phone_no.data
    db.session.commit()
    flash(f'Success! {attemped_id.first_name}  details is updated', category='success')
    return redirect(url_for('<employee>.employee'))
    