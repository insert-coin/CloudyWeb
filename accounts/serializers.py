from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', )
