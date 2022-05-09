from django.urls import path
from .views import LoginAPI, UserAPI, LogoutAPI, CountriesAPI,\
    SaleStatisticsAPI, SaleAPI, UpdateSaleAPI, UploadSaleData
# from drf_yasg.views import get_schema_view # Commented-out line as it
# was not in use
# from drf_yasg import openapi # Commented-out line of code as it was 
# not in use


# BUG:
##### BELOW PIECE OF CODE IS COMMENTED-OUT BECAUSE drf_yasg SWAGGER WAS
##### NOT LETTING TO DEPLOY THE APPLICATION ON HEROKU

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Backend Developer Trial Assignment Login/Logout API",
#       default_version='v1',
#       description="This is the API for Meistry Global Teams' Backend\
#            Developer Trial Assignment, where a use can create \
#                account, log in and enter personal details with a CSV\
#                     file.",
#       terms_of_service="#",
#       contact=openapi.Contact(email="khubikhawar@gmail.com"),
#       license=openapi.License(name="Khubaib Khawar"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

##### COMMENTED-OUT CODE ENDS HERE

urlpatterns = [
    path('api/v1/login/', LoginAPI.as_view()),
    path('api/v1/user/', UserAPI.as_view()),
    path('api/v1/logout/', LogoutAPI.as_view()),
    path('api/v1/users/<int:id>/', UserAPI.as_view()),
    path('api/v1/countries/', CountriesAPI.as_view()),
    path('api/v1/sale_statistics/', SaleStatisticsAPI.as_view()),
    path('api/v1/sales/', SaleAPI.as_view(), name='sales'),
    path('api/v1/sales/<int:id>/', UpdateSaleAPI.as_view()),
    path('sales/upload/', UploadSaleData.as_view()),
]