from django.urls import path,include
from search.views import SearchView
from .import views
urlpatterns = [
    path('',SearchView.as_view(), name='search' ),
]