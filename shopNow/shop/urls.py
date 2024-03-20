from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    path('register/',views.register ,name='register'),
    path('login/',views.login_page ,name='login'),
    path('logout/',views.logout_page ,name='logout'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart_page/', views.cart_page, name='cart_page'),
    path('fav/', views.fav_page, name='fav'),
    path('fav_view_page/', views.fav_view, name='fav_view_page'),
    path('remove_fav/<str:cid>', views.remove_fav, name='remove_fav'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),
    path('collections/',views.collections ,name='collections'),
    path('collections/<str:name>',views.collectionsview ,name='collections'),
    path('collections/<str:category>/<str:product>',views.product_details ,name='product_details'),

]