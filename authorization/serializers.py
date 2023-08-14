from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'password')

    def save(self):
        password = self.validated_data.pop('password', None)
        if password:
            self.validated_data['password'] = make_password(password)

        return super().save()
