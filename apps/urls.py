from django.urls import path, include


urlpatterns = [
    path('common/', include('apps.common.urls'), name='common'),
    path('user/', include('apps.user.urls'), name='user'),
    path('teacher/', include('apps.teacher.urls'), name='teacher'),
    # path('management/', include('apps.management.urls'), name='management'),
    # path('center/', include('apps.center.urls'), name='center'),
]
