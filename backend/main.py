from flask import Flask, jsonify, request, send_file
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime
import os
import random
import time

from models import USER, CUSTOMER, PROFESSIONAL, SERVICE, SERVICEREQUEST, db

from worker import celery_init_app

from celery import shared_task
from celery.result import AsyncResult
from celery.schedules import crontab

import flask_excel as excel

from flask_caching import Cache

from tasks import make_csv_request, send_email_to_professional, monthly_reminder_to_customers

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["JWT_SECRET_KEY"] = "JWT_SECRET"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'database.db')

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = "Content-Type"

celery_app = celery_init_app(app)

excel.init_excel(app)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "ruralclap",
    "CACHE_REDIS_URL": "redis://localhost:6379/3"
}

app.config.from_mapping(config)
cache = Cache(app)

####################################################################################

# scheduled tasks

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(hour=19, minute=0),
        crontab(hour=18, minute=59),
        send_email_to_professional.s()
    )

@celery_app.on_after_configure.connect
def send_monthly_summary(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(hour=0, minute=0, day_of_month=1),
        crontab(hour=18, minute=59),
        monthly_reminder_to_customers.s()
    )

####################################################################################

# APIs 

class Register(Resource):
    def post(self):
        data = request.get_json()
        emailId = data.get('emailId')
        password = data.get('password')
        role = data.get('role')

        # print('data ', data)

        if role == 'customer':
            address = data.get('address')
            phone_number = data.get('phone_number')
        elif role == 'professional':
            service_type = data.get('service_type')
            experience = data.get('experience')
        else:
            return jsonify({'message': 'Wrong Role!'})
        
        if USER.query.filter_by(emailId=emailId).first():
            return jsonify({'message': "User already exists! Try logging in"})
    
        user = USER(emailId=emailId, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        if role=='customer':
            customer = CUSTOMER(user_id=user.id, address=address, phone_number=phone_number)
            db.session.add(customer)
        elif role=='professional':
            professional = PROFESSIONAL(user_id=user.id, service_type=service_type, experience=experience)
            db.session.add(professional)
        
        db.session.commit()
        return jsonify({'message': 'User created'})

    def get(self):
        return jsonify({"message": "GET request of /register"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        emailId = data.get('emailId')
        password = data.get('password')
        role = data.get('role')

        user = USER.query.filter_by(emailId=emailId).first()

        # print(user)

        if user:
            if user.password == password:
                if user.role == role:
                    access_token = create_access_token(identity={"emailId": emailId, "role": role})
                    if user.role=='customer':
                        customer = CUSTOMER.query.filter_by(user_id=user.id).first()
                        return jsonify({"message": "Login Successful", "token":access_token, "is_blocked":customer.is_blocked})
                    elif user.role=='professional':
                        professional = PROFESSIONAL.query.filter_by(user_id=user.id).first()
                        return jsonify({"message": "Login Successful", "token":access_token, "is_blocked":professional.is_blocked})
                    elif user.role == "admin":
                        return jsonify({"message": "Login Successful", "token": access_token, "is_blocked":False})
                else:
                    return jsonify({"message": "Wrong Role, try with another role or register with appropriate role"})
            else:
                return jsonify({"message": "Wrong Password"})
        else:
            return jsonify({"message": "User does not exist! Try registering"})

    def get(self):
        return jsonify({"message": "GET of /login"})
    
class GetUsers(Resource):
    @cache.cached(timeout=20)
    def get(self):
        
        pre_customers = CUSTOMER.query.all()
        customers = [c.to_dict() for c in pre_customers]
        
        pre_professionals = PROFESSIONAL.query.all()
        professionals = [p.to_dict() for p in pre_professionals]

        return jsonify({'message': 'Successful', 'customers': customers, 'professionals': professionals})

    def post(self):

        data = request.get_json()
        user_id = data.get('user_id')
        is_blocked = data.get('is_blocked')

        role = USER.query.filter_by(id=user_id).first().role

        if role=='customer':
            customer = CUSTOMER.query.filter_by(user_id=user_id).first()
            customer.is_blocked = is_blocked
            db.session.commit()
        elif role=='professional':
            professional = PROFESSIONAL.query.filter_by(user_id=user_id).first()
            professional.is_blocked = is_blocked
            db.session.commit()
        else:
            return jsonify({'message': "some error in role"})

        return jsonify({'message': 'success'})

class IsAccepted(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        email = current_user.get('emailId')

        professional = PROFESSIONAL.query.join(USER).filter_by(emailId=email).first()

        if professional.is_approved == False:
            return jsonify({'message': "You have not been approved by the admin yet. Please wait until admin approves your profile"})
        else:
            return jsonify({'message': "Approved"})
        
class ProfessionalRequests(Resource):
    def get(self):
        pre_professionals = PROFESSIONAL.query.filter_by(is_approved=False).all()
        professionals = [pr.to_dict() for pr in pre_professionals]
        # print(type(professionals))
        # print(professionals)
        return jsonify({'message': "Got requests", 'professionals': professionals})
    
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        # print(user_id)
        profo = PROFESSIONAL.query.filter_by(user_id=user_id).first()
        # print(profo)
        profo.is_approved = True
        db.session.commit()

        return jsonify({'message': "Professional {} approved!".format(user_id)})
    
class AddService(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        name = data.get('name')
        desc = data.get('description')
        time_req = data.get('time_required')
        base_price = data.get('base_price')

        service = SERVICE(name=name, price=base_price, time_required=time_req, description=desc)
        db.session.add(service)
        db.session.commit()

        return jsonify({'message': 'Service added successfully'})

class UpdateService(Resource):
    def post(self):
        data = request.get_json()

        service_id = data.get('service_id')
        print(service_id)   
        name = data.get('name')
        time_required = data.get('time_required')
        price = data.get('price')
        description = data.get('description')

        try:
            service = SERVICE.query.filter_by(id=service_id).first()

            service.name = name
            service.time_required = time_required
            service.price = price
            service.description = description

            db.session.commit()
        except:
            print(data)

        return jsonify({'message': "Updated Service"})

class DeleteService(Resource):
    def post(self):
        data = request.get_json()
        service_id = data.get('service_id')

        # print(service_id)

        try:
            service = SERVICE.query.filter_by(id=service_id).first()
            db.session.delete(service)
            db.session.commit()
        except:
            print(service_id)
        
        return jsonify({'message': "Service has been deleted"})

class GetServicesBySearch(Resource):
    def post(self):
        data = request.get_json()
        serviceName = data.get('serviceName')

        # print('backend: got this service name: {}'.format(serviceName))

        search = '%{}%'.format(serviceName)

        result = SERVICE.query.filter(SERVICE.name.like(search)).all()

        # print(result)

        services = [s.to_dict() for s in result]

        # print(services)

        return jsonify({'message':'Got searched services', 'services':services})

class GetUsersBySearch(Resource):
    def post(self):
        data = request.get_json()

        emailId = data.get('username')

        search = '%{}%'.format(emailId)

        c = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(search)).all()
        p = db.session.query(PROFESSIONAL).join(USER).filter(USER.emailId.like(search)).all()

        customers = [cs.to_dict() for cs in c]
        professionals = [ps.to_dict() for ps in p]

        return jsonify({'message': 'got searched users', 'customers': customers, 'professionals': professionals})

class BookService(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        # print(current_user)
        user_email_id = current_user['emailId']

        data = request.get_json()
        date = datetime.strptime(data.get('date'), "%Y-%m-%d")
        service_id = data.get('service_id')
        professional_id = data.get('professional_id')

        print('backend got this date', date)
        print('backend got service_id', service_id)
        print('backend got this professional id', professional_id)

        customer = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(user_email_id)).first()

        print(customer)

        service_request = SERVICEREQUEST(
            service_id=service_id, 
            customer_id=customer.user_id, 
            professional_id=professional_id,
            date_of_request=date
        )

        db.session.add(service_request)

        print('done')

        db.session.commit()

        print('commited')

        return jsonify({'message': 'Service requested successfully'})

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        customer_email = current_user['emailId']

        customer = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(customer_email)).first()

        pre_sreqs = SERVICEREQUEST.query.filter_by(customer_id=customer.user_id).all()

        sreqs = [srq.to_dict() for srq in pre_sreqs]

        return jsonify({'message': 'Here are service requests for this user', 'service_requests': sreqs})

class DeleteServiceRequest(Resource):
    def post(self):
        data = request.get_json()
        print(data)

        id = data['id']

        sreq = SERVICEREQUEST.query.filter_by(id=id).first()

        db.session.delete(sreq)

        db.session.commit()

        return jsonify({'message': 'Service request successfully deleted'})

class ProfServiceRequests(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        email = current_user['emailId']
        prof = db.session.query(PROFESSIONAL).join(USER).filter(USER.emailId.like(email)).first()

        pre_prof_ser_reqs = SERVICEREQUEST.query.filter_by(professional_id=prof.user_id).all()

        prof_ser_reqs = [psr.to_dict() for psr in pre_prof_ser_reqs]

        return jsonify({'message': "got professional's service requests", 'prof_ser_reqs': prof_ser_reqs})

class Request(Resource):
    def get(self):
        id = request.args.get('id')
        type = request.args.get('type')

        req = SERVICEREQUEST.query.filter_by(id=id).first()

        if type == 'accept':
            req.service_status = 'accepted'
        elif type == 'reject':
            req.service_status = 'rejected'
        elif type == 'close':
            req.service_status = 'closed'

        db.session.commit()

        return jsonify({'message': 'Service request {} {}ed'.format(id, type)})
    
class GetMe(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        email = current_user['emailId']

        user = USER.query.filter_by(emailId=email).first()

        if user.role == 'admin':
            customers = [c.to_dict() for c in CUSTOMER.query.all()]
            professionals = [p.to_dict() for p in PROFESSIONAL.query.all()]
            services = [s.to_dict() for s in SERVICE.query.all()]
            service_requests = [sr.to_dict() for sr in SERVICEREQUEST.query.all()]

            return jsonify({
                'customers': customers, 
                'professionals': professionals, 
                'services': services,
                'service_requests': service_requests
            })
        
        elif user.role == 'customer':
            my_details = db.session.query(CUSTOMER).join(USER).filter(USER.emailId==email).first().to_dict()
            service_requests = [sr.to_dict() for sr in SERVICEREQUEST.query.filter_by(customer_id=my_details['user_id']).all()]
            return jsonify({
                'me': my_details,
                'my_service_requests': service_requests
            })
        
        elif user.role == 'professional':
            my_details = db.session.query(PROFESSIONAL).join(USER).filter(USER.emailId==email).first().to_dict()
            service_requests = [sr.to_dict() for sr in SERVICEREQUEST.query.filter_by(professional_id=my_details['user_id']).all()]
            return jsonify({
                'me': my_details,
                'my_service_requests': service_requests
            })

class AddRemarks(Resource):
    def post(self):
        data = request.get_json()
        service_request_id, remarks, rating = data['id'], data['remarks'], data['rating']

        sreq = SERVICEREQUEST.query.filter_by(id=service_request_id).first()

        sreq.remarks = remarks

        sreq.rating = rating

        db.session.commit()

        return jsonify({'message': 'Review submitted successfully!'})

class UpdateRequest(Resource):
    def post(self):
        data = request.get_json()
        service_request_id, date = data['id'], data['date']

        sreq = SERVICEREQUEST.query.filter_by(id=service_request_id).first()

        sreq.date_of_request = datetime.strptime(date, "%Y-%m-%d")

        db.session.commit()

        return jsonify({'message': 'Request updated successfully'})

class StartCSVRequest(Resource):
    def get(self):
        task = make_csv_request.delay()
        return jsonify({'task_id': task.id})

class GetCSVByTaskId(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        result = AsyncResult(task_id)
        if result.ready():
            filename = result.result
            # print(filename)
            return send_file(filename, download_name='export.csv', as_attachment=True)
        else:
            return jsonify({"message": "Task is still pending..."}), 404

class CacheDemo(Resource):
    @cache.cached(timeout=10)
    def get(self):
        time.sleep(5)
        return 'Hi, this is a cached value: '+str(random.randint(1,100))
#############################################################################

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetUsers, '/getUsers')
api.add_resource(IsAccepted, '/isaccepted')
api.add_resource(ProfessionalRequests, '/professionalrequests')
api.add_resource(AddService, '/addservice')
api.add_resource(UpdateService, '/updateservice')
api.add_resource(DeleteService, '/deleteservice')
api.add_resource(GetServicesBySearch, '/getservices')
api.add_resource(GetUsersBySearch, '/getusersbysearch')
api.add_resource(BookService, '/bookservice')
api.add_resource(DeleteServiceRequest, '/deleteservicerequest')
api.add_resource(ProfServiceRequests, '/getprofserreqs')
api.add_resource(Request, '/request')
api.add_resource(GetMe, '/getme')
api.add_resource(AddRemarks, '/addremarks')
api.add_resource(UpdateRequest, '/updatedate')

api.add_resource(StartCSVRequest, '/startcsvrequest')
api.add_resource(GetCSVByTaskId, '/getcsvbytaskid')

api.add_resource(CacheDemo, '/cachedemo')

#############################################################################
with app.app_context():
    db.create_all()

    # creating admin if admin does not exist
    if not USER.query.filter_by(emailId="admin@gmail.com", password="admin", role="admin").first():
        admin = USER(emailId="admin@gmail.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
