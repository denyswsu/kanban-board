from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "url", "is_active", "is_staff", "is_superuser")

        extra_kwargs = {
            "url": {"view_name": "api:users-detail", "lookup_field": "username"}
        }


class CreateUserSerializerCaseInsensitive(UserSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        read_only_fields = (
            "id", "name", "url", "is_active", "is_staff", "is_superuser"
        )

    def validate(self, attrs):
        self._validate_passwords(attrs)
        return attrs

    @staticmethod
    def _validate_passwords(attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))

    @staticmethod
    def validate_email(email):
        email = email.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(_("User with this Email already exists."))
        return email

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            is_active=False
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user
