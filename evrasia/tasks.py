from .extensions import celery, mail
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPRecipientsRefused

@celery.task(name='task.email')
def send_async_email(msg_dict):
    msg = Message()
    msg.__dict__.update(msg_dict)
    try:
        mail.send(msg)
    except SMTPRecipientsRefused:
        return "Email invalid!"

def msg_to_dict(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=app.config['EVRASIA_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['EVRASIA_MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    return msg.__dict__

def send_email(to, subject, template, **kwargs):
    send_async_email.delay(msg_to_dict(to, subject, template, **kwargs))