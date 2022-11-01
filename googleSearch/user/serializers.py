from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from user.models import Search

from rest_framework import serializers, validators
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    confirmpass = serializers.CharField(
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirmpass',
                  'email', 'first_name', 'last_name')

        # unable to write the password by serializer email is unique
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A User with this Name Already Exists"
                    )
                ]
            }
        }

    # creating new user
    def create(self, validated_data):
        username = validated_data.get('username')
        password = make_password(validated_data.get('password'))
        confirmpass = make_password(validated_data.get('confirmpass'))
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        confirmpass = validated_data.pop('confirmpass')

        user = User.objects.create(
            username=username,
            password=password,
            # confirmpass=confirmpass,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def validate(self, data):
        if data.get('password') != data.get('confirmpass'):
            raise serializers.ValidationError("Please enter a password or "
                                              "password is not matching.")
        return data


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ('user', 'search_data', 'created_at')


class ViewAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ('search_data', )
        # ordering = ('-created_at', )
class SaveDataSerializer(serializers.ModelSerializer):

    class Meta:
        model:Search
        fields = ('search_data', )
