from django.urls import path, include
from .import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('cart', views.AddToCartViewSet)

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),

    path('', views.MyTemplateView.as_view(), name='index'),

    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('create_category/', views.CreateIndividualCategory.as_view(), name='create_category'),
    path('update_category/<int:category_id>/', views.UpdateIndividualCategory.as_view(), name='update_category'),
    path('delete_category/<int:category_id>/', views.DeleteIndividualCategory.as_view(), name='delete_category'),

    path('product/<int:category_id>', views.ProductListView.as_view(), name='product_list'),
    path('detail_product/<int:product_id>', views.ProductDetailView.as_view(), name='product_detail'),
    path('create_product/', views.CreateIndividualProduct.as_view(), name='create_product'),
    path('update_product/<int:product_id>/', views.UpdateIndividualProduct.as_view(), name='update_product'),
    path('delete_product/<int:product_id>/', views.DeleteIndividualProduct.as_view(), name='delete_product'),

    path('cartitem/', views.CartItemListView.as_view(), name='cartitem_list'),
    path('add-to-cart/<int:product_id>/',views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart-item/update/<int:pk>/', views.CartItemUpdateView.as_view(), name='cartitem_update'),
    path('cart-item/delete/<int:pk>/', views.CartItemDeleteView.as_view(), name='cartitem_delete'),

    path('api/', include(router.urls))

]
