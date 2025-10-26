from django.urls import path
from .views import (
    ShopListView,
    ShopDetailView,
    ShopProductsView,
    ShopCategoriesView,
    ShopAvailabilityView,
    ShopReviewListCreateView,
    ShopReviewDetailView,
    ShopsByCategoryView,
    NearbyShopsView,
    ShopSearchView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Shops
    path("shops/", ShopListView.as_view(), name="shop-list"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shop-detail"),
    path("shops/<int:pk>/products/", ShopProductsView.as_view(), name="shop-products"),
    path("shops/<int:pk>/categories/", ShopCategoriesView.as_view(), name="shop-categories"),
    path("shops/<int:pk>/availability/", ShopAvailabilityView.as_view(), name="shop-availability"),

    # Shop Reviews
    path("shops/<int:shop_id>/reviews/", ShopReviewListCreateView.as_view(), name="shop-reviews"),
    path("reviews/<int:pk>/", ShopReviewDetailView.as_view(), name="shop-review-detail"),

    # Categories
    path("shops-by-category/", ShopsByCategoryView.as_view(), name="shops-by-category"),

    # Nearby Shops
    path("shops/nearby/", NearbyShopsView.as_view(), name="nearby-shops"),
    path("shops/search/", ShopSearchView.as_view(), name="shop-search"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)