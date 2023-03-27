from django.core.mail import EmailMessage
from django.conf import settings
from config import celery_app


class EmailService:
    @celery_app.task
    def send_email(
        self, message, recipient_list, subject="Notification from Kanban Board",
        from_email=settings.DEFAULT_FROM_EMAIL, cc_list=None, bcc_list=None,
        reply_to=None, html_message=None, headers=None, attachments=None
    ):
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            cc=cc_list,
            bcc=bcc_list,
            reply_to=reply_to,
            headers=headers,
        )
        self.add_html_message(email, html_message)
        self.add_attachments(email, attachments)
        email.send()

    @staticmethod
    def add_html_message(email, html_message):
        if html_message:
            email.content_subtype = "html"
            email.body = html_message

    @staticmethod
    def add_attachments(email, attachments):
        for attachment in attachments or []:
            email.attach_file(attachment)
