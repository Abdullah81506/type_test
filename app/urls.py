from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Home page route
    path('typing/', views.typing_test, name='typing_test'), # Typing test route
    path('save_result/', views.save_result, name='save_result'), # Route to save typing results
    path('results/', views.results, name='results'), # Route to display typing results   
    path('get_paragraph/', views.get_paragraph, name='get_paragraph'), # Route to get a paragraph for typing test

]
