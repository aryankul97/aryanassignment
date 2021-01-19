from django.contrib import admin
from django.urls import path
from app.views import ProcessPayment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/processpayment/', ProcessPayment),
]