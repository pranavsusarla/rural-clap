from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class USER(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailId = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer', 'professional'

    def to_dict(self): # easy to send to frontend
        return {
            'id': self.id,
            'email_id': self.emailId,
            'role': self.role
        }
        
# Customer Model
class CUSTOMER(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    # emailId = db.Column(db.String(80), db.ForeignKey('user.emailId'), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)
    user = db.relationship('USER', backref=db.backref('customer')) #, foreign_keys=[user_id, emailId])

    def to_dict(self):
        return {
            'customer_id': self.id,
            'user_id': self.user_id,
            'email_id': self.user.emailId,
            'role': self.user.role,
            'address': self.address,
            'phone_number': self.phone_number,
            'is_blocked': self.is_blocked,
        }

# Professional Model
class PROFESSIONAL(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    # emailId = db.Column(db.String(80), db.ForeignKey('user.emailId'), unique=True, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    user = db.relationship('USER', backref=db.backref('professional')) #, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'professional_id': self.id,
            'user_id': self.user_id,
            'email_id': self.user.emailId,
            'role': self.user.role,
            'service_type': self.service_type,
            'experience': self.experience,
            'is_blocked': self.is_blocked,
            'is_approved': self.is_approved
        }

# Service Model
class SERVICE(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return{
            'service_id': self.id,
            'name': self.name,
            'price': self.price,
            'time_required': self.time_required,
            'description': self.description
        }

class SERVICEREQUEST(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete="CASCADE"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id', ondelete="CASCADE"), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=True, default=0)
    service_status = db.Column(db.String(20), nullable=False, default="open")  # open, accepted, closed, rejected
    remarks = db.Column(db.String(200), nullable=True)

    service = db.relationship('SERVICE', backref='service_request')#, cascade="all, delete-orphan")
    customer = db.relationship('CUSTOMER', backref='service_request')#, cascade="all, delete-orphan")
    professional = db.relationship('PROFESSIONAL', backref='service_request')#, cascade="all, delete-orphan")

    def to_dict(self):
        return{
            'service_request_id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id,
            'date_of_request': self.date_of_request,
            'service_status': self.service_status,
            'remarks': self.remarks,
            'price': self.service.price,
            'rating': self.rating
        }