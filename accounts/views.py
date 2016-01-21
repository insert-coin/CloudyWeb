from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import permissions as drf_permissions

from . import serializers
from . import permissions

User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return (drf_permissions.AllowAny(),)
        else:
            return (permissions.IsStaffOrSelf(),)



