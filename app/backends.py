from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Account
from django.contrib.auth.models import User

class AccountBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = Account.objects.get(username=username)
            if account.status == 'locked':
                # Nếu tài khoản bị khóa, trả về None
                return None
            elif check_password(password, account.password):
                user, created = User.objects.get_or_create(username=account.username, email=account.email)
                user.account_role = account.role  # Add this line to store the role in the user instance
                return user
        except Account.DoesNotExist:
            pass  # Không cần xử lý ở đây, hãy để nó trả về None mặc định

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            account = Account.objects.get(username=user.username)
            user.account_role = account.role  # Add this line to store the role in the user instance
            return user
        except User.DoesNotExist:
            return None