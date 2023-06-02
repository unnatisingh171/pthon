from flask import Blueprint,render_template,redirect,url_for,flash,jsonify, request
from app.forms import UpdateForm,SearchForm
from app.models import Employee
from app import db
from flask_login import login_required
from datetime import date
from flask_restful import Resource,Api
from sqlalchemy import  or_

admin=Blueprint("app",__name__,static_folder="static",template_folder="templates")
employee_json = []
class Search(Resource):
    def get(self,search_value):
        global employee_json
        employee = Employee.query.filter(or_(Employee.first_name.like(search_value + "%"),Employee.address.like(search_value + "%"))).all()
        for value in employee:
            content = {"first_name": value.first_name, "last_name": value.last_name, "email": value.email,
                       "phone_number": value.phone_number,
                       "dob": value.dob, "address": value.address}
            employee_json.append(content)
        return redirect(url_for("<admin>.search_data"))

@admin.route("/search_data",methods=['POST','GET'])
def search_data():
    form=SearchForm()
    if form.validate_on_submit():
        global employee_json
        employee_json = []
        return redirect(url_for("search",search_value=form.search.data))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template("admin/admin.html",values=employee_json,form=form)
@admin.route("/admin",methods=['POST','GET'])
@login_required
def Admin():
    form=SearchForm()
    values=Employee.query.all()
    employee_json=[]
    for value in values:
        content={"first_name":value.first_name,"last_name":value.last_name,"email":value.email,"phone_number":value.phone_number,
                 "dob":value.dob,"address":value.address}
        employee_json.append(content)
    if form.validate_on_submit():
        return redirect(url_for("search",search_value=form.search.data))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template("admin/admin.html",values=employee_json,form=form)

@admin.route("/detail/<employee>",methods=['POST','GET'])
@login_required
def detail(employee):
    employee_details=Employee.query.filter_by(email=employee).first()
    return render_template("admin/detail.html",employee_details=employee_details)

@admin.route("/detail/detail_update/<employee_email>",methods=['POST','GET'])
@login_required
def detail_update(employee_email):
    employee_details=Employee.query.filter_by(email=employee_email).first()
    form=UpdateForm()
    if form.validate_on_submit():
        update_check(form,employee_details)
    else:
        form.first_name.data=employee_details.first_name
        form.last_name.data=employee_details.last_name
        form.email.data=employee_details.email
        form.phone_no.data=employee_details.phone_number
        cr_date =employee_details.dob.split('-')
        form.dob.data=date(int(cr_date[0]),int(cr_date[1]),int(cr_date[2]))
        form.address.data=employee_details.address
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(err_msg,category='danger')
    return render_template('admin/detail_update.html',form=form,first_name=employee_details.first_name)

def update_check(form,employee_details):
    attemped_email=Employee.query.filter_by(id=employee_details.id).first()
    attemped_email.first_name=form.first_name.data
    attemped_email.last_name=form.last_name.data
    attemped_email.dob=form.dob.data
    attemped_email.address=form.address.data
    attemped_email.phone_number=form.phone_no.data
    db.session.commit()
    values=Employee.query.all()
    values.pop()
    print(type(values))
    flash(f'Successfully! {employee_details.first_name}  details is updated', category='success')
    return redirect(url_for("<admin>.Admin"))


@admin.route("/delete/<employee>",methods=['POST','GET'])
@login_required
def delete(employee):
    employee_details=Employee.query.filter_by(email=employee).delete()
    flash(f'Successfully! {employee}  details is deteled', category='success')
    db.session.commit()
    return redirect(url_for("<admin>.Admin"))