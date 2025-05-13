from users.models import *
from rest_framework import serializers
from .utils import send_email_verification
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "code"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.set_password(validated_data["password"])
        user.save()

        RoleRelated.objects.create(user=user, role=Role.get_student())
        send_email_verification(user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        roles = Role.objects.filter(rolerelated__user=instance)
        data["roles"] = RoleSerializer(roles, many=True).data
        return data

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["password"]
        password = serializers.CharField(min_length=6, write_only=True)
        
