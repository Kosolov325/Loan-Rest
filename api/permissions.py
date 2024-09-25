from rest_framework import permissions


class IsOwnerOrReject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user


class IsOwnerOfLoanOrReject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.loan.client == request.user