from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Device


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Username should not contain spaces.")
        return value

    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value
    
    def validate_email(self, value):
        # if "@example.com" not in value:
        #     raise serializers.ValidationError("Email must be from the domain example.com.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    public_key_pem = serializers.JSONField(required=False)
    device_id = serializers.CharField(max_length=100, required=False)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        public_key_pem = attrs.get('public_key_pem')
        device_id = attrs.get('device_id', None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")
        
        Device.objects.update_or_create(
            user=user,
            device_id=device_id,
            defaults={'public_key_pem': public_key_pem,
                      'is_active': True}
        )

        refresh = RefreshToken.for_user(user)

        return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
