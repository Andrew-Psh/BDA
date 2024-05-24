from flask import Blueprint, render_template, redirect, url_for, request
from flask_mail import Message
from app import mail

mail_routes = Blueprint('mail_routes', __name__)

@mail_routes.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']

        message = Message(subject=subject, recipients=[recipient], body=body)
        try:
            mail.send(message)
            return "Email sent!"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('send_email.html')

# Другие роуты, связанные с отправкой почты, могут быть добавлены здесь