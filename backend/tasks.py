from celery import shared_task
from models import SERVICEREQUEST, CUSTOMER, PROFESSIONAL, SERVICE
import flask_excel as excel

from mail_service import sendmail

# CELERY TASKS
@shared_task(ignore_result=False)
def make_csv_request():
    sreqs = SERVICEREQUEST.query.all()

    csv_output = excel.make_response_from_query_sets(sreqs, [
        "id",
        "service_id",
        "customer_id",
        "professional_id",
        "date_of_request",
        "service_status",
        "remarks",
        "rating"
    ], "csv")

    filename="generated_csvs/admin_report.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)
    
    return str(filename)

@shared_task(ignore_result=False)
def send_email_to_professional():
    professionals = PROFESSIONAL.query.all()
    emails = [[p.to_dict()['email_id'], p.to_dict()['user_id']] for p in professionals]
    for email, id in emails:
        pending_requests = len(SERVICEREQUEST.query.filter_by(professional_id=id, service_status='open').all())
        print(email, pending_requests)
        if pending_requests>0:
            subject = 'Daily Check In | RuralClap'
            content = '''
            <html>
                <body>
                    <div>
                        <h2 style="color: #dc3545;">Pending Service Requests!</h2>
                        <p>Hello <strong>{}</strong>,</p>
                        <p>You have <strong>{}</strong> pending service requests that need your attention.</p>
                        <p>Don't miss out on these opportunities to grow your business.</p>
                        <p><a href="http://localhost:8081" class="btn">View Pending Requests</a></p>
                        <p>We look forward to your response.</p>
                        <p>Best Regards,<br> RuralClap</p>
                    </div>
                </body>
                </html>
            '''.format(email, pending_requests)
            sendmail(email, subject, content)
        else:
            subject = 'Daily Check In | RuralClap'
            content = '''
            <html>
                <body>
                    <div>
                        <p>Hello <strong>{}</strong>,</p>
                        <p>You have no pending requests today!!</p>
                        <p><a href="http://localhost:8081" class="btn">Visit RuralClap</a></p>
                        <p>We look forward to your response.</p>
                        <p>Best Regards,<br> RuralClap</p>
                    </div>
                </body>
                </html>
            '''.format(email)
            sendmail(email, subject, content)
    return "Sent daily reminder to professionals"

@shared_task(ignore_result=False)
def monthly_reminder_to_customers():
    customers = CUSTOMER.query.all()
    emails = [[c.to_dict()['email_id'], c.to_dict()['user_id']] for c in customers]
    for email, id in emails:
        sreqs = SERVICEREQUEST.query.filter_by(customer_id=id).all()
        requested_services = len(sreqs)
        closed_services = len([s for s in sreqs if s.to_dict()['service_status'] == 'closed'])
        print(email, requested_services, closed_services)
        # total_spent = sum([s.to_dict()['price'] for s in SERVICE.query.all()])
        subject = 'Monthly Summary | RuralClap'
        content = '''
            <html>
                <body>
                    <div>
                        <h2 style="color: #007bff;">Service Summary</h2>
                        <p>Hello <strong>{}</strong>,</p>
                        <p>Here is your service summary:</p>
                        <ul>
                            <li><strong>Service Requests:</strong> {}</li>
                            <li><strong>Closed Requests:</strong> {}</li>
                        </ul>
                        <p>Best Regards,<br> RuralClap</p>
                    </div>
                </body>
                </html>
                '''.format(email, requested_services, closed_services) # should be html
        sendmail(email, subject, content)
    
    return "Sent monthly summary to customers"
