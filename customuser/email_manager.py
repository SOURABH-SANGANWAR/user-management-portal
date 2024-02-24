
from django.core.mail import send_mail
from django.conf import settings


class EmailManager:

    @staticmethod
    def welcome_email(user):
        subject = "Welcome to our platform!"
        body = f"Dear {user.first_name},\n\nWelcome to our platform! We are excited to have you on board.\n\nBest regards,\nThe Team"
        send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])
    
    @staticmethod
    def send_otp(user, otp):
        subject = "Send OTP"
        body = f"Dear {user.first_name},\n\nPlease use the following OTP to verify your email address: {otp}\n\nBest regards,\nThe Team"
        send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])

    @staticmethod
    def password_reset_email(user, link):
        subject = "Password Reset"
        body = f"Dear {user.first_name},\n\nWe have received a request to reset your password. Please click on the link below to reset your password. {link}\n\nBest regards,\nThe Team"
        send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])