from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "User with this username already exists."})

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop("password2", None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def validate_email(self, value):
        request = self.context.get("request", "")
        user = request.user

        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value

    def validate_username(self, value):
        request = self.context.get("request", "")
        user = request.user

        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already in use")
        return value


class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match")

        return attrs

    def validate_old_password(self, value):
        request = self.context.get("request", "")

        if not request.user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):
        request = self.context.get("request", "")
        user = request.user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                "You dont have permission to edit this user's password")

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
