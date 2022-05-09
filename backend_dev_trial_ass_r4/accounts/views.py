from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from uritemplate import partial
from .models import Detail, Country, City, Sale
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import LoginSerializer, DetailSerializer, CountrySerializer,\
    SaleSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .forms import SalesDataForm
import numpy as np
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginAPI(generics.CreateAPIView):
    """
    This class creates the API for Login of a user.

    '''

    Attributes
    ----------
    permission_classes : rest-framework.permissions Object
        a variable to store the value of permissions
    serializer_class : LoginSerializer Class's Object
        a variable to attach a specific Serialezer with this API.
    
    Methods
    -------
    post(request, *args, **kwargs)
        stores the user's data after serializing and validating it.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Step 1:
            Gets the serialzed data of the user, entered in frontend 
            of API.
        Step 2:
            Stores that data in 'serialzer' variable and validate it.
        Step 3:
            Saves the validated 'data' Object (a dictionary) in the 
            variable 'user'.

        Parameters
        ----------
        request : DRF HTTP POST Request Object
            data entered by the user on the frontend of the DRF
            REST API.

        Returns
        ------
        Dictionary
            a dictionary holding the values of the keys 'token' and 
            'user_id'.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            "token": str(token),
            "user_id": user.id
        })


class LogoutAPI(generics.ListAPIView): 
    """
    This class creates the API for Logout of a user.

    '''

    Methods
    -------
    get(request)
        logs out the user.
    """

    def get(request):
        """
        Logs out the user

        Parameters
        ----------
        request : DRF HTTP POST Request Object
            data entered by the user on the frontend of the DRF
            REST API.

        Returns
        ------
        Dictionary
            a dictionary the message.
        """

        request.user.auth_token.delete()

        return Response('User Logged out successfully')


class UserAPI(generics.RetrieveUpdateAPIView):
    """
    This class creates the API for User.

    '''

    Attributes
    ----------
    permission_classes : list
        a list to define who should have access to this API
    serializer_class : UserSerializer Class's Object
        a variable to attach a specific Serialezer with this API
    
    Methods
    -------
    get_object(request, id)
        returns value stored in 'user' key of 'request', a DRF HTTP
        POST Object (a dictionary).
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = DetailSerializer
    http_method_names = ["get", "patch"]

    def get(self, request, id):
        user = User.objects.get(pk=1)
        detail = Detail.objects.get(user=user)
        
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'gender': detail.gender,
            'age': detail.age,
            'country': detail.country,
            'city': detail.city

        }

        return Response(data)

    def patch(self, request, id):
        user = User.objects.get(pk=1)     
        details = Detail.objects.get(user=user)
        details_data = {}

        # if "gender" in request.data.keys():
        #     details_data["gender"] = request.data["gender"]

        # if "age" in request.data.keys():
        #     details_data["age"] = request.data["age"]

        # if "country" in request.data.keys():
        #     details_data["Country"] = request.data["country"]
        
        # if "city" in request.data.keys():
        #     details_data["city"] = request.data["city"]

        serializer = DetailSerializer(details, data=details_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return JsonResponse(data="wrong parameters", safe=False)


class CountriesAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get(request, *args, **kwargs):
        countries = Country.objects.all()

        record = []

        for country in countries:
            data = {
            'id': 0,
            'name': 'n',
            'cities': []
            }

            data['id'] = country.id
            data['name'] = country.name

            cities = City.objects.all()

            for city in cities:
                if city.object_id == data['id']:
                    data['cities'].append({
                        'id': city.id,
                        'name': city.name
                        })

            record.append(data)
            
        full_data = {"COUNTRIES": record}

        return Response(full_data)


class SaleStatisticsAPI(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get(self, request):
        token = request.user.auth_token.key
        email = str(request.user.auth_token.user)
        current_user = User.objects.get(email=email)
        all_users_sales = Sale.objects.all()
        current_user_sales = Sale.objects.filter(user=current_user)
        current_user_total_revenue = 0.0
        current_user_total_sales = 0.0
        all_users_total_revenue = 0.0
        all_users_total_sales = 0.0
        current_user_highest_selling_product = ''
        current_user_revenues = []

        for sale in current_user_sales:
            current_user_total_revenue += float(sale.revenue)
            current_user_total_sales += float(sale.sales_number)
            current_user_revenues.append(float(sale.revenue))

        for sale in all_users_sales:
            all_users_total_revenue += float(sale.revenue)
            all_users_total_sales += float(sale.sales_number)

        current_user_highest_revenue = np.max(current_user_revenues)
        product_sales = []
        
        for sale in current_user_sales:
            product_sales.append(sale.sales_number)
            revenue = float(sale.revenue)

            if revenue == current_user_highest_revenue:
                current_user_highest_revenue_id = sale.id
                current_user_highest_revenue_prod = sale.product

        highest_selling = np.max(product_sales)
        current_user_highest_selling_product = current_user_sales.filter(sales_number=highest_selling)

        data = {
            "average_sales_for_current_user": current_user_total_revenue /\
                 current_user_total_sales,
            "average_sale_all_user": all_users_total_revenue /\
                 all_users_total_sales,
            "highest_revenue_sale_for_current_user": {
                "sale_id": current_user_highest_revenue_id,
                "revenue": current_user_highest_revenue
            },
            "product_highest_revenue_for_current_user": {
                "product_name": current_user_highest_revenue_prod,
                "price": int(current_user_highest_revenue)
            },
            "product_highest_sales_number_for_current_user": {
                "product_name": current_user_highest_selling_product[0].product,
                "price": int(current_user_highest_selling_product[0].revenue)
            }
        }

        return Response(data)


class SaleAPI(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get(self, request):
        record = []
        data = {}
        email = str(request.user.auth_token.user)
        user = User.objects.get(email=email)
        sales = Sale.objects.filter(user=user)

        for sale in sales:
            record.append(
                {
                    "id": int(sale.id),
                    "product": str(sale.product),
                    "revenue": str(sale.revenue),
                    "sales_number": int(sale.sales_number),
                    "date": str(sale.date),
                    "user_id": int(user.id),
                }
            )

        data = {
            "DATA": record
        }
        
        return Response(data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale_data = serializer.validated_data

        email = str(request.user.auth_token.user)
        user = User.objects.get(email=email)

        try:
            sale_obj = Sale.objects.create(
                date=sale_data['date'],
                product=sale_data['product'],
                revenue=sale_data['revenue'],
                sales_number=sale_data['sales_number'],
                user=user
            )
            
            data = {
                "id": sale_obj.id,
                "product": sale_obj.product,
                "revenue": float(sale_obj.revenue),
                "sales_number": sale_obj.sales_number,
                "date": sale_obj.date,
                "user_id": user.id
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
        
        except:
            data = {
                "error": "Could not create Sale Object"
            }
            
            return Response(data)

class UpdateSaleAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    http_method_names = ["put", "delete", "patch"]

    def delete(self, request, id):
        try:
            sale_obj = Sale.objects.get(id=id)
            sale_obj.delete()

            data = {
                "message": "Successfully deleted Sale Object"
            }

            return Response(data, status=status.HTTP_204_NO_CONTENT)

        except:
            data = {
                "error": "Sale object does not exists at " + str(id) + " id"
            }

            return Response(data)

    def patch(self, request, id):
        email = str(request.user.auth_token.user)
        user = User.objects.get(email=email)
        sale_obj, _ = Sale.objects.get_or_create(id=id)

        try:
            sale_data = {}

            if "product" in request.data.keys():
                sale_data["product"] = request.data["product"]

            if "revenue" in request.data.keys():
                sale_data["revenue"] = request.data["revenue"]

            if "sales_number" in request.data.keys():
                sale_data["sales_number"] = request.data["sales_number"]

            if "date" in request.data.keys():
                sale_data["date"] = request.data["date"]

            serializer = SaleSerializer(sale_obj, data=sale_data, partial=True)

            print(serializer)
        
            if serializer.is_valid():
                serializer.save()

                sale_obj, _ = Sale.objects.get_or_create(id=id)
                
                data = {
                    "id": sale_obj.id,
                    "product": sale_obj.product,
                    "revenue": sale_obj.revenue,
                    "sales_number": sale_obj.sales_number,
                    "date": sale_obj.date,
                    "user_id": user.id

                }
                
                return Response(data, status.HTTP_200_OK)
        
        except:
            data = {
                "error": "Could not update Sale Object"
            }
            
            return Response(data)
        

    def put(self, request, id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale_data = serializer.validated_data
        email = str(request.user.auth_token.user)
        user = User.objects.get(email=email)
        sale_obj, _ = Sale.objects.get_or_create(id=id)        

        try:            
            sale_obj.date = sale_data['date']            
            sale_obj.product = sale_data['product']            
            sale_obj.revenue = sale_data['revenue']            
            sale_obj.sales_number = sale_data['sales_number']

            sale_obj.save()
            
            data = {
                "id": sale_obj.id,
                "product": sale_obj.product,
                "revenue": sale_obj.revenue,
                "sales_number": sale_obj.sales_number,
                "date": sale_obj.date,
                "user_id": user.id

            }
            
            return Response(data, status.HTTP_200_OK)
        
        except:
            data = {
                "error": "Could not update Sale Object"
            }
            
            return Response(data)


class UploadSaleData(View):
    template_name = 'accounts/salesdata.html'

    def get(self, request):
        form = SalesDataForm()
        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        CSV_DATA = []
        DATA_USER_EMAIL = ''

        DATA_USER_EMAIL = str(request.POST['email'])
        file = request.FILES['csv'].read().decode('utf-8')
        data = file.split('\n')
        data = data[1 : -1]

        for rec in data:
            CSV_DATA.append(rec.split(','))
        
        try:
            user = User.objects.get(email=DATA_USER_EMAIL)

            for rec in CSV_DATA:
                Sale.objects.get_or_create(
                    date=rec[0],
                    product=rec[1],
                    sales_number=rec[2],
                    revenue=rec[3],
                    user=user
                    )
            
            context = {
                'msg': "CSV data"
            }

            return render(request, 'accounts/uploaded.html', context)

        except:
            context = {
                'msg': "User does not exists at " + DATA_USER_EMAIL + \
                    ". CSV data could not be"
            }

            return render(request, 'accounts/uploaded.html', context)
