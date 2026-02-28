from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from apps.consumption.mongo_utils import get_mongo_collection

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'status')
        read_only_fields = ('id', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # Bypass Djongo INSERT (SQLDecodeError on auth user insert); use pymongo directly
        col = get_mongo_collection('authentication_user')
        # Next integer id (existing users have integer id from assign_ids / Django)
        cursor = col.find({}).sort('id', -1).limit(1)
        doc = next(cursor, None)
        new_id = (doc['id'] + 1) if (doc and doc.get('id') is not None) else 1
        now = datetime.utcnow()
        email = User.objects.normalize_email(validated_data['email'])
        user_doc = {
            'id': new_id,
            'password': make_password(validated_data['password']),
            'last_login': None,
            'is_superuser': False,
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': email,
            'role': 'user',
            'status': 'active',
            'is_active': True,
            'is_staff': False,
            'created_at': now,
            'updated_at': now,
        }
        col.insert_one(user_doc)
        return User.objects.get(pk=new_id)
