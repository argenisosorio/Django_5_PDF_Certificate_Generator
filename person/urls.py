from django.urls import path
from . import views

# Define the application namespace for URL reversing
# This helps distinguish URLs between different apps when using 'url' template tag
app_name = 'person'

# URL patterns for the Person CRUD (Create, Read, Update, Delete) operations
urlpatterns = [
    # Home/List view: Displays all person records
    # URL: /
    # View: home - Shows listing of all persons
    path('', views.home, name='home'),

    # Create view: Form for creating new person records
    # URL: /create/
    # View: create_person - Handles person creation form
    path('create/', views.create_person, name='create'),

    # Detail view: Shows details of a specific person
    # URL: /<pk>/ (e.g., /1/)
    # View: detail_person - Displays single person details
    # <int:pk> - Captures the person's primary key as integer
    path('<int:pk>/', views.detail_person, name='detail'),

    # Update view: Form for editing existing person records
    # URL: /<pk>/update/ (e.g., /1/update/)
    # View: update_person - Handles person update form
    path('<int:pk>/update/', views.update_person, name='update'),

    # Delete view: Handles person record deletion
    # URL: /<pk>/delete/ (e.g., /1/delete/)
    # View: delete_person - Handles deletion confirmation
    path('<int:pk>/delete/', views.delete_person, name='delete'),
]