from django.contrib.auth.models import User
from rest_framework import serializers

from shop.models import Item, Category


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#     password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True,
#                                       validators=[validate_password])
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'email')
#
#     def validate(self, attrs):
#         if attrs.get('password1') != attrs.get('password2'):
#             raise serializers.ValidationError({"password": "error password"})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#         )
#
#         user.set_password(validated_data['password1'])
#         user.save()
#         return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'phoneNumber', 'bio', 'last_name', 'first_name', 'money']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "model", "name", "photo", "memory", "description", "money", "category"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
