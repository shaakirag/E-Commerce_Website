from django.urls import path
from . import views

app_name = "staff"
urlpatterns = [
    path('staff/login', views.loginPage, name="login"),
    path('staff/logout', views.logoutUser, name="logout"),
    path('staff/orders', views.index, name="index"),
    path('staff/delete_order/<str:pk>/', views.deleteOrder, name="delete-order"),
    path('staff/update_order/<str:pk>/', views.updateOrder, name="update-order"),
    path('staff/customers/', views.customers, name="customers"),
    path('staff/customers/registered/<str:pk>/', views.registered_profile, name="registered-profile"),
    path('staff/customers/guest/<str:pk>/', views.guest_profile, name="guest-profile"),
    path('staff/create_product/', views.createProduct, name="create-product"),
    path('staff/add_images/<str:pk>', views.addImages, name="add-images"),
    path('staff/update_product/<str:pk>/', views.updateProduct, name="update-product"),
    path('staff/delete_product/<str:pk>/', views.deleteProduct, name="delete-product"),
    path('staff/products/', views.products, name="products"),
    path('staff/products/details/<str:pk>/', views.product_details, name="product-details"),
]