from django.urls import path
from .views import (SignUpManagerView, UserLoginView, EmployeeRegistrationView,
                    UserProfile, UpdateProfile, UpdateEmployeeProfile, AllEmployees, ActiveEmployee)


urlpatterns = [
    path('signup_manager', SignUpManagerView.as_view(), name='signup_manager'),
    path('signup_employee', EmployeeRegistrationView.as_view(),
         name='signup_employee'),
    path('login', UserLoginView.as_view(), name='login'),
    path('update_manager_profile', UpdateProfile.as_view(),
         name='update_manager_profile'),
    path('employees/', AllEmployees.as_view(), name='all_employees'),
    path('employees/<int:pk>',
         UpdateEmployeeProfile.as_view(), name='employees'),
    path('profile', UserProfile.as_view(), name='profile'),
    path('active_employee/<int:pk>',
         ActiveEmployee.as_view(), name='active_employee'),
]
