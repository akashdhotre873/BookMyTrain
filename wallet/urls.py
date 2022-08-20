from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_money, name="get_details"),
    path('mybookings/', views.mybookings, name="mybookings"),
    path('cancel_ticket/<int:id>', views.cancel_ticket, name="cancel_ticket")
]