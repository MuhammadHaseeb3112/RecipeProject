from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
# ======================
# ADMIN
# ======================
    path('admin/', admin.site.urls),

# ======================
# MAIN APP
# ======================    
    path('', include('RecipeApp.urls')),

# ======================
# AUTH: LOGIN / LOGOUT
# ======================
    path('accounts/login/', auth_views.LoginView.as_view(
    template_name='registration/login.html',
    redirect_authenticated_user=True
), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
    next_page='login'
), name='logout'),

# ======================
# PASSWORD RESET
# ======================
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
    template_name='registration/password_reset_form.html'
), name='password_reset'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='registration/password_reset_done.html'
), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='registration/password_reset_confirm.html'
), name='password_reset_confirm'),

    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='registration/password_reset_complete.html'
), name='password_reset_complete'),

# ======================
# PASSWORD CHANGE (LOGGED-IN USERS)
# ======================
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
    template_name='registration/password_change_form.html',
    success_url='/accounts/password_change/done/'   # ✅ ensures redirect
), name='password_change'),

    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='registration/password_change_done.html'
), name='password_change_done'),

]

# ======================

# STATIC + MEDIA (DEV ONLY)

# ======================

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
