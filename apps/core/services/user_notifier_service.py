from typing import Iterable

from django.contrib.auth import get_user_model

from core.services import EmailService

User = get_user_model()


class UserNotifierService:
    def __init__(self, users: Iterable[User], params: dict):
        self.users = users
        self.params = params
        self.notification = self.build_message()

    def notify(self):
        EmailService().send_email(**self.notification)

    def build_message(self):
        return {
            "recipient_list": [user.email for user in self.users],
            "subject": self.params.get("subject"),
            "message": self.params.get("message"),
            "html_message": self.params.get("html_message"),
        }
