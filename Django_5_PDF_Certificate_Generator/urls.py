from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include the URLs person pdf_generator app.
    path('', include('pdf_generator.urls')),
]
