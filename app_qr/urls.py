from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_qr.views import CategoryList,CategoryDetail, ProductDetail, ProductList, AllProducCategorytList, ResturantData, ResturantList, ResturantDetail,QrList, AllCategory,AllProduct,AllProducCategorytListPublic



urlpatterns = [

    path('allproductscategorypublic/<int:pk>', AllProducCategorytListPublic.as_view(), name='allproductspublic'),
    path('allproductscategory/', AllProducCategorytList.as_view(), name='allproducts'),
    path('category/', CategoryList.as_view(), name='category-create'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='category'),
    path('product/', ProductList.as_view(), name='product-create'),
    path('product-list/<int:pk>', AllProduct.as_view(), name='product-list'),
    path('category-list/<int:pk>', AllCategory.as_view(), name='category-list'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product'),
    path('resturant/', ResturantList.as_view(), name='resturant-create'),
    path('resturant/<int:pk>', ResturantDetail.as_view(), name='resturant'),
    path('resturant-data/', ResturantData.as_view(), name='resturant'),
    path('qr/', QrList.as_view(), name='qr'),
  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)