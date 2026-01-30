from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
def home(request):
    return HttpResponse("Student Management System Backend is Running 🚀")
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    # Student APIs
    path('api/', include('student_app.urls')),

    # Login APIs (JWT)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
