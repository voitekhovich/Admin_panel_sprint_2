from django.urls import include, path

urlpatterns = [
    path('api/', include('movies.api.urls')),
]
