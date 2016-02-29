from rest_framework import permissions

class OperatorOnly(permissions.BasePermission):

    # create: operator only
    # list & retrieve: all authenticated users
    # update & partial_update: operator only
    # destroy: operator only

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated()
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return True

class UserIsOwnerOrOperator(permissions.BasePermission):

    # create: own or operator only
    # list & retrieve: own or operator only
    # update & partial_update: own or operator only
    # destroy: own or operator only

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated() and \
            ((request.user.username == request.data['user']) or \
                request.user.is_staff)
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user == obj.user)

class UserIsOwnerOrOperatorExceptUpdate(permissions.BasePermission):

    # create: own or operator only
    # list & retrieve: own or operator only
    # update & partial_update: no one is allowed
    # destroy: own or operator only

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated() and \
            ((request.user.username == request.data['user']) or \
                request.user.is_staff)
        elif view.action in ['update', 'partial_update']:
            return False
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user == obj.user)