from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.gis.geos import fromstr
from rest_framework import serializers

from users.utils import Util

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)
    is_swiped = serializers.SerializerMethodField(read_only=True)

    def get_is_swiped(self, obj):
        user = self.context['request'].user
        return obj.is_swiped(user)

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(
            instance)
        pnt = fromstr(ret['location'])
        ret['location'] = {'longitude': pnt.coords[0],
                           'latitude': pnt.coords[1]}
        return ret

    class Meta:
        fields = ('id', 'first_name', 'last_name',
                  'email', 'avatar', 'gender', 'password', 'is_swiped',
                  'location')
        extra_kwargs = {'password': {'write_only': True,
                                     'validators': [validate_password]},
                        'id': {'read_only': True},
                        'locations': {'read_only': True},

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
