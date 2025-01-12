from uuid import UUID

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action

from django.contrib.auth.hashers import check_password

from .models import User
from .permissions import UserPermissions
from .validations import validate_password_strength
from .serializers import ListUserSerializer, CreateUserSerializer, UpdateUserRoleSerializer, ChangePasswordSerializer

class ServiceHealthView(APIView):
    def get(self, request: Request):
        return Response({
            "message": "API is up and running"
        }, status=status.HTTP_200_OK)
    

class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True).all()
    lookup_field = 'uuid'
    permission_classes = [UserPermissions]
    default_serializer_class = ListUserSerializer
    serializer_classes = {
        'create': CreateUserSerializer
    }

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.default_serializer_class
    
    @action(methods=['GET'], detail=False, url_path="me")
    def get_me_details(self, request: Request):
        serializer = ListUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['PATCH'], detail=False, url_path="role")
    def update_role(self, request: Request):
        serializer = UpdateUserRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.BAD_REQUEST)
        
        user = User.objects.filter(uuid=serializer.validated_data.get("uuid")).first()
        if not user:
            return Response({
                "message": "Invalid user UUID"
            }, status=status.BAD_REQUEST)
        
        user.role = serializer.validated_data.get("role")
        user.save()

        return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['PUT'], url_path="deactivate")
    def deactivate_account(self, request: Request, uuid: UUID):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response({
                "message": "Invalid user UUID"
            }, status=status.BAD_REQUEST)
        
        user.is_active = False
        user.save()
        return Response({"message": "User account deactivated successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['PUT'], url_path="change-password")
    def change_password(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        old_pass = serializer.validated_data.get("old_password")
        new_pass = serializer.validated_data.get("new_password")
        confirm_pass = serializer.validated_data.get("confirm_password")

        new_pass_errors = validate_password_strength(new_pass)
        if len(new_pass_errors):
            return Response({
                "new_password": new_pass_errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(old_pass, request.user.password):
            return Response({
                "message": "Invalid old password"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if old_pass == new_pass:
            return Response({
                "message": "Old password and new password cannot be the same"
            }, status=status.HTTP_200_OK)
        
        if new_pass != confirm_pass:
            return Response({
                "message": "New password and confirm password must be same"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.set_password(new_pass)
        request.user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)