from users.models import *
from rest_framework import serializers
from clubs.serializers import ClubSerializer    

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
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()

        RoleRelated.objects.create(user=user, role=Role.get_student())
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        roles = Role.objects.filter(rolerelated__user=instance)
        data["roles"] = RoleSerializer(roles, many=True).data
        return data

        
