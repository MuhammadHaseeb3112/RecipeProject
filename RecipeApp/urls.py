from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # ======================
    # MAIN PAGES
    # ======================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # ======================
    # RECIPES
    # ======================
    path('recipes/', views.recipe_list, name='recipes'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:id>/rate/', views.submit_rating, name='submit_rating'),
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),

    path("my-recipes/", views.my_recipes, name="my_recipes"),
    path("recipe/<int:id>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:id>/delete/", views.delete_recipe, name="delete_recipe"),
    path('recipe/<int:id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # ======================
    # USER PROFILE
    # ======================
    path("profile/", views.profile, name="profile"),

    # ======================
    # AUTH (ONLY CUSTOM PART)
    # ======================
    path('signup/', views.signup_view, name='signup'),

    # Logout (optional override)
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]