from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.common import views

app_name = "common"

router = DefaultRouter()

urlpatterns = [
    path("region/", views.RegionListView.as_view(), name="region"),
    path("district/", views.DistrictListView.as_view(), name="district"),
    path("neighborhood/", views.NeighborhoodListView.as_view(), name="neighborhood"),

    path('media/create/', views.MediaCreateAPIView.as_view(), name='media-create'),

]
