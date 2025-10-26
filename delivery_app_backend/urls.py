from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from login.views import GoogleLogin


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('delivery.urls')), 
    path('api/', include('industries.urls')),
    path('api/', include('categories_app.urls')),
    path('api/', include('products_app.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('wishlist.urls')),
    # path('api/', include('order.urls')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),



    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),  # required for social login
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('api/phone-auth/', include('login.urls'),name='phone_login'),


    path('api/profile/', include('user_profile.urls'),name='about_me'),



    

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
