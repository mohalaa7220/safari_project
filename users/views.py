from rest_framework import generics, views
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (SignUpManagerSerializer, SignUpEmployeeSerializer,
                          UserManagerProfile, EmployeeSerializerProfile, UpdateManagerSerializer, UpdateEmployeeSerializer)
from .serializer_error import serializer_error
from .models import User
from project.permissions import IsManager
from .cursorPagination import UsersPagination
from .UsersFilter import UserFilter
from django_filters import rest_framework as filters


# ---------- SignUp Manager View
class SignUpManagerView(generics.GenericAPIView):
    serializer_class = SignUpManagerSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            data_serializer = UserManagerProfile(
                user, context={"request": request}).data
            token = Token.objects.create(user=user).key
            return Response(data={"message": "User Created Successfully", "data": data_serializer, 'token': token}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)


class EmployeeRegistrationView(generics.GenericAPIView):
    serializer_class = SignUpEmployeeSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user).key
            return Response(data={"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)


# ----- Login ------
class UserLoginView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'message': 'Email or Password incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        if user.role == 'employee':
            serializer = EmployeeSerializerProfile(
                user, context={'request': request})
        elif user.role == 'manager':
            serializer = UserManagerProfile(user, context={'request': request})
        return Response({
            "message": "Login Successfully",
            "data": serializer.data,
            "token": token.key}, status=status.HTTP_200_OK)


# Profile
class UserProfile(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'employee':
            serializer = EmployeeSerializerProfile(
                user, context={'request': request})
        elif user.role == 'manager':
            serializer = UserManagerProfile(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Update Profile Manager
class UpdateProfile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user = request.user
        serializer = UpdateManagerSerializer(
            instance=user, data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)


# Update profile employee
class UpdateEmployeeProfile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.all()
    serializer_class = EmployeeSerializerProfile

    def update(self, request, pk=None):
        employee = self.get_object()
        serializer = UpdateEmployeeSerializer(
            instance=employee, data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)

    def delete(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = False
        employee.save()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_200_OK)


# Get all employees
class AllEmployees(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.filter(role='employee')
    serializer_class = EmployeeSerializerProfile
    pagination_class = UsersPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_hired')


class ActiveEmployee(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.all()

    def update(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = True
        employee.save()
        return Response({"message": "User active successfully"}, status=status.HTTP_200_OK)
