from django.urls import path
from . import views

urlpatterns = [
    path('<int:train_id>/<int:trainroute_source_id>/<int:trainroute_destination_id>', views.check_seats, name="check_seats"),
    path('get_details/<int:max_seat_no>/<int:train_id>/<int:trainroute_source_id>/<int:trainroute_destination_id>/<str:coach_type>', views.get_details, name="get_details")
]