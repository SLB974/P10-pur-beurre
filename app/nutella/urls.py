from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:pk>/", views.product, name="product"),
    path("product_search/", views.search_product, name="product_search"),
    path('product_replacement/<int:pk>/', views.search_replacement, name="product_replacement"),
    path('save_favorite/<int:pk_replaced>/<int:pk_replacing>/', views.save_favorite, name="save_favorite"),
    path('delete_favorite/<int:pk>/', views.delete_favorite, name="delete_favorite"),
    path('product_user/<int:pk>/', views.product_user, name="product_user"),
    path("legal_notice", views.legal_notice, name="legal_notice"),
]
