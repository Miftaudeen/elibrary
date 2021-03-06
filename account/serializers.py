from rest_framework import serializers

from account.models import User
from account.permission import get_as_perm
from account.perms_constants import PERM_CHOICES


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=PERM_CHOICES)
    username = serializers.CharField(max_length=60, allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role']

    def save(self, username):
        user, _ = User.objects.update_or_create(
                                   email=self.validated_data.get('email'),
                                   defaults={
                                       'first_name': self.validated_data.get('first_name'),
                                       'last_name': self.validated_data.get('last_name'),
                                       'phone_number': self.validated_data.get('phone_number'),
                                       'username': username
                                   })
        return user


class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']

    def save(self):
        user, _ = User.objects.update_or_create(
            email=self.validated_data.get('email'),
            defaults={
                'first_name': self.validated_data.get('first_name'),
                'last_name': self.validated_data.get('last_name'),
                'phone_number': self.validated_data.get('phone_number'),
                'username': self.validated_data.get('username')
            })
        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'roles', 'temp_password']


class UserPasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    old_password = serializers.CharField(max_length=250)
    new_password = serializers.CharField(max_length=250)
