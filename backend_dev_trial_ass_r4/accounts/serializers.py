from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import CharField, IntegerField
from .models import Detail, City, Country, Sale
from rest_framework import serializers


class MainUserSerializer(serializers.ModelSerializer):
    """
    This class creates a Serializer to serialize the data of a user.

    '''

    Attributes
    ----------
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.
    """

    class Meta:
        """
        This class creates defines the meta data of MainUserSerializer 
        class.

        '''

        Attributes
        ----------
        model : User Model Object
            a variable to sore User Model Name
        fields : list
            a variable to store the list of names of fields
        """

        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    
class CitySerializer(serializers.ModelSerializer):
    """
    This class creates a Serializer to serialize the data of a cities.

    '''

    Attributes
    ----------
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.
    """

    class Meta:
        """
        This class creates defines the meta data of CitySerializer 
        class.

        '''

        Attributes
        ----------
        model : City Model Object
            a variable to sore City Model Name
        fields : list
            a variable to store the list of names of fields
        """
        model = City
        fields = ('name',)


class CountrySerializer(serializers.ModelSerializer):
    """
    This class creates a Serializer to serialize the data of a countries.

    '''

    Attributes
    ----------
    city : CitySerializer Objecy
        a variable to store the CitySerializer Name
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.
    """

    # city = CitySerializer()

    class Meta:
        """
        This class creates defines the meta data of CountrySerializer 
        class.

        '''

        Attributes
        ----------
        model : Country Model Object
            a variable to sore Country Model Name
        fields : list
            a variable to store the list of names of fields
        """
        model = Country
        fields = "__all__"


class DetailSerializer(serializers.ModelSerializer):
    """
    This class creates a Serializer to serialize the data of a user.

    '''

    Attributes
    ----------
    usr : MainUserSerializer Object
        a variable to store the MainUserSerializer Name
    country : CountrySerializer Objecy
        a variable to store the CountrySerializer Name
    city : CitySerializer Object
        a variable to store the CitySerializer Name
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.

    Methods
    -------
    update(self, instance, validated_data)
        updates the instances Ciy, Country and Detail tables
    """

    usr = MainUserSerializer()
    # country = CountrySerializer()
    # city = CitySerializer()

    class Meta:
        """
        This class creates defines the meta data of UserSerializer 
        class.

        '''

        Attributes
        ----------
        model : Detail Model Object
            a variable to sore Detail Model Name
        fields : list
            a variable to store the list of names of fields
        """

        model = Detail
        fields = ["gender", "age", "country", "city", "usr"]

    def update(self, instance, validated_data):
        """
        Returns an string

        Parameters
        ----------
        self : UserSerializer Class Object
            an instance of UserSerializer class
        instance : Detail Class Object
            an instance of Detail class
        validated_data : list
            a list of entered data by user in UserSerializer

        Returns
        ------
        Detail Class Instance
            an instacne of Detail class
        """

        instance = super().update(instance, validated_data)
        
        instance.save()
            
        return instance


class LoginSerializer(serializers.Serializer):
    """
    This class creates a Serializer to serialize the data of a user.

    '''

    Attributes
    ----------
    email : serializers.EmailField Object
        a variable to store the email as a string
    password : serializers.CharField Objecy
        a variable to store the password as a string
    city : CitySerializer Object
        a variable to store the CitySerializer Name
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.

    Methods
    -------
    validate(self, data)
        validates the data entered by user in LoginSerializer
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Returns an string

        Parameters
        ----------
        self : LoginSerializer Class Object
            an instance of LoginSerializer class
        data : list
            an instance of Detail class
        validated_data : list
            a list of entered data by user in LoginSerializer

        Returns
        ------
        User Model Instance
            an instacne of User Model
        """

        user = authenticate(**{
            'username': data['email'],
            'password': data['password']
            })

        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class SaleSerializer(serializers.ModelSerializer):
    """
    This class creates a Serializer to serialize the data of sales.

    '''

    Attributes
    ----------
    Meta : user defined type
        a type/class to define the meta-data of this specific 
        Serializer.
    """

    class Meta:
        """
        This class creates defines the meta data of SaleSerializer 
        class.

        '''

        Attributes
        ----------
        model : Sale Model Object
            a variable to sore Sale Model Name
        fields : list
            a variable to store the list of names of fields
        """

        model = Sale
        fields = ('date', 'product', 'revenue', 'sales_number')