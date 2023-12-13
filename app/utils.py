from django.core.mail import send_mail
from django.conf import settings



def send_verification_email(submission, request_type):

    if request_type == 'request demo':
        subject = 'Intellisense Demo Request'
        message = f'Thank you for your request, {submission.Full_name} . We will review it shortly.'
    elif request_type == 'contact':
        subject = 'Contact-us request'
        message = f'Thank you for your request, {submission.Full_name} . We will review it shortly.'
    elif request_type == 'help and support':
        # Handle other request types or provide a default message
        subject = 'User Request for HelpandSupport'
        message = f'Thank you for your request, {submission.Full_name} . We will review it shortly.'
    else:
        # Handle other request types or provide a default message
        subject = 'User Request Verification'
        message = 'Thank you for your request,{submission.Full_name} . We will review it shortly.'

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [submission.Business_email]

    send_mail(subject, message, from_email, recipient_list)


def ForgotPassword_verification_email(email,request_type):
    if request_type == 'ForgotPassword':
        # Forgot Password email
        user_subject = 'Forgot Password : Reset Request'
        user_message = 'We have received request to reset your Intellisense account password. We will review it shortly'

        # Support team email
        support_subject = 'New Forgot Password Request'
        support_message = f'A new Forgot Password request has been submitted by {email}.'

        from_email = settings.EMAIL_HOST_USER  # email configured for sending notifications to user and intellisense support team
        user_recipient_list = [email]  # Automtically gets replaced with the actual user's email address
        support_recipient_list = ['amol.nevase@beautosys.com']  # Replace with the actual support team's email address

        # Send email to the user
        send_mail(user_subject, user_message, from_email, user_recipient_list)

        # Send email to the support team
        send_mail(support_subject, support_message, from_email, support_recipient_list)