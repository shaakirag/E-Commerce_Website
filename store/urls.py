from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
	path('', views.index, name="index"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/<str:pk>', views.userProfile, name="profile"),
    path('user/settings/<str:pk>', views.userSettings, name="settings"),
    path('user/settings/<str:pk>/password_reset', views.passwordChange, name="password-change"),
    path('register/', views.register, name="register"),
    path('products/', views.products, name="products"),
    path('products/details/<int:id>/', views.product_details, name="product_details"),
    path('products/details/<int:pk>/update_review/<int:id>/', views.updateReview, name="update_review"),
    path('delete_review/', views.deleteReview, name="delete_review"),
    path('categories/', views.categories, name="categories"),
    path('categories/<int:id>/', views.category_products, name="category_products"),
    path('tags/', views.tags, name="tags"),
    path('tags/<int:id>/', views.tag_products, name="tag_products"),
    path('favourites/<str:pk>/', views.favourites, name="favourites"),
    path('update_fav/', views.updateFav, name="update_fav"),
	path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_item_quantity/', views.updateItemQuantity, name="update_item_quantity"),
	path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processOrder, name="process_order"),
]