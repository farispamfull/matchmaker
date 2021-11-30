from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.utils import Util

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name',
                  'email', 'avatar', 'gender', 'password',)
        extra_kwargs = {'password': {'write_only': True,
                                     'validators': [validate_password]},
                        'id': {'read_only': True},
                        'gender': {'required': True}, }

        model = User

    def create(self, validated_data):
        email = Util.normalize_email(validated_data['email'])
        validated_data['email'] = email
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        validators=[validate_password],
        required=True)
    current_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data['current_password']
        user = self.context['request'].user
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Неверный пароль"})
        return data
