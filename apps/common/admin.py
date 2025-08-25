from django.contrib import admin
from .models import Region, District, Neighborhood, Media


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "name", "is_active", "is_deleted", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active", "is_deleted")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "region", "name", "is_active", "is_deleted", "created_at")
    search_fields = ("name", "region__name")
    list_filter = ("region", "is_active", "is_deleted")


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "district", "name", "is_active", "is_deleted", "created_at")
    search_fields = ("name", "district__name", "district__region__name")
    list_filter = ("district", "is_active", "is_deleted")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "file_name", "file_type", "is_active", "is_deleted", "created_at")
    search_fields = ("file_name",)
    list_filter = ("file_type", "is_active", "is_deleted")
