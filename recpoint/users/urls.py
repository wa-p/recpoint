from django.urls import path

from recpoint.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    v_list_view,
)

app_name = "users"
urlpatterns = [
    path("", view=user_list_view, name="list"),
    path("vehicles/", view=v_list_view, name="v_list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
