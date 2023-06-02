from app import app,db,login_manager
from app import bcrypt
from flask_login import UserMixin
from datetime import date

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Employee(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column("first_name",db.String(100),nullable=False)
    last_name=db.Column("last_name",db.String(100),nullable=False)
    email=db.Column("email",db.String(100),nullable=False,unique=True)
    password_hash=db.Column("password",db.String(100),nullable=False)
    dob=db.Column("dob",db.String(100),nullable=False)
    address=db.Column("address",db.String(100),nullable=False)
    phone_number=db.Column("phone_number",db.String(100),nullable=False)
    
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __init__(self,first_name,last_name,dob,address,email,phone_number,password):
        self.first_name=first_name
        self.last_name=last_name
        self.dob=dob
        self.address=address
        self.email=email
        self.phone_number=phone_number
        self.password=password
    def __repr__(self):
        return self.first_name
def admin_create():
    today = date.today()
    email_check=Employee.query.filter_by(email="admin@xyz.com").first()
    if not email_check:
        admin_details = Employee(first_name="admin",last_name="admin",
                                    email="admin@xyz.com",password="123456",
                                    dob=today,address=" ",phone_number=" ")
        db.session.add(admin_details)
        db.session.commit()
with app.app_context():
    db.create_all()
    admin_create()
