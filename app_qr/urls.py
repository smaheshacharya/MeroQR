from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_qr.views import CategoryList, CategoryDetail, ProductDetail, ProductList, AllProducCategorytList


urlpatterns = [

    path('allproductscategory/<int:pk>', AllProducCategorytList.as_view(), name='allproducts'),
    path('category/', CategoryList.as_view(), name='category-create'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='category'),
    path('product/', ProductList.as_view(), name='product-create'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)