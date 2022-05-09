from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserManager(BaseUserManager):
    """
    This class creates the Manager/Handler for User Model.

    '''
    
    Methods
    -------
    _create_user(self, email, password, is_staff, 
    is_superuser, **extra_fields)
        this method creates the user based on the parameters passed 
        to it
    create_user(self, email, password, **extra_fields)
        this method uses the _create_user() method to create the user
    create_superuser(self, email, password, **extra_fields)
        this method uses the _create_user() method to create super user
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates a user based on parameters passed to it

        Parameters
        ----------
        self : UserManager Class Object
            an instance of UserManager class
        email : string
            data entered by user as an email
        password : string
            data entered by user as a password
        is_staff : bool
            choice selected by user
        is_superuser : bool
            choice selected by user
        **extra_fields : variable of any type
            extraa parameters entered by user

        Returns
        ------
        User Model Object
            an instance of User Model Object
        """

        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)

        user = self.model(
            username=email,
            email=email,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Creates a user based on parameters passed to it

        Parameters
        ----------
        self : UserManager Class Object
            an instance of UserManager class
        email : string
            data entered by user as an email
        password : string
            data entered by user as a password
        **extra_fields : variable of any type
            extraa parameters entered by user

        Returns
        ------
        User Model Object
            an instance of User Model Object
        """

        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a super user based on parameters passed to it

        Parameters
        ----------
        self : UserManager Class Object
            an instance of UserManager class
        email : string
            data entered by user as an email
        password : string
            data entered by user as a password
        **extra_fields : variable of any type
            extraa parameters entered by user

        Returns
        ------
        User Model Object
            an instance of User Model Object
        """

        user=self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    This class creates a new user. This is a custom User Model.

    '''
    
    Attributes
    ----------
    username : string
        a variable to store username
    email : string
        a variable to store email
    first_name : string
        a variable to store first name
    last_name : string
        a variable to store last name
    is_staff : bool
        a variable to store the staff status
    is_superuser : bool
        a variable to store super user status
    is_active : string
        a variable to store active status
    last_login : DateTime Object
        a variable to store date and time
    date_joined : DateTime object
        a variable to store date and time
    USERNAME_FIELD : stirng
        a variable to store the field name
    EMAIL_FIELD : string
        a variable to store field name
    REQUIRED_FIELDS : list
        a variable to store the list of field names
    objects : UserManager Object
        a variable to store an instance of UserManager Object    

    Methods
    -------
    get_absolute_url(self)
        a method to return the url to User Object instance
    """

    username = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        """
        Returns an absolute url to the User Object instance

        Parameters
        ----------
        self : User Class Object
            an instance of User class

        Returns
        ------
        String
            a url to the User Model instance
        """

        return "/users/%i/" % (self.pk)


class City(models.Model):
    """
    This class creates the City Table for storing City names.

    '''
    
    Attributes
    ----------
    name : models.CharField Object
        a variable to store a name as a string
    country : models.ForeignKey Object
        a variable to store the Foriegn Key of Country Table

    Methods
    -------
    __str__(self)
        returns the string
    """

    name = models.CharField(max_length=100 ,default='')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        """
        Returns an string

        Parameters
        ----------
        self : Country Class Object
            an instance of Country class

        Returns
        ------
        String
            a customized string
        """

        return ("{} ({})".format(self.name, self.content_object))


class Country(models.Model):
    """
    This class creates the Country Table for storing Country names.

    '''
    
    Attributes
    ----------
    name : models.CharField Object
        a variable to store a name as a string

    Methods
    -------
    __str__(self)
        returns the string
    """

    name = models.CharField(max_length=100, default='')
    cities = GenericRelation(City)

    def __str__(self):
        """
        Returns an string

        Parameters
        ----------
        self : Country Class Object
            an instance of Country class

        Returns
        ------
        String
            a customized string
        """

        return ("{}".format(self.name))


class Detail(models.Model):
    """
    This class creates the Detail Table for storing user details.

    '''
    
    Attributes
    ----------
    user : models.OneToOneField
        a variable to One to One relation of City Table with User Table
    gender : models.CharField Object
        a variable to store the gender as a string
    age : models.IntegerField
        a variable to store age as an integer
    country : models.IntegerField
        a variable to store country number as an integer
    city : models.IntegerField
        a variable to store city number as an integer

    Methods
    -------
    __str__(self)
        returns the string
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default='')
    age = models.IntegerField(default=0)
    country = models.IntegerField(default=1)
    city = models.IntegerField(default=1)

    def __str__(self):
        """
        Returns an string

        Parameters
        ----------
        self : Country Class Object
            an instance of Country class

        Returns
        ------
        String
            a customized string
        """

        return ("{} ({} {})".format(self.user.email, self.user.first_name, self.user.last_name))


class Sale(models.Model):
    """
    This class creates the Sale Table for sales.

    '''
    
    Attributes
    ----------
    date : models.CharField
        a variable to store date as a string
    product : models.CharField Object
        a variable to store the product name as a string
    revenue : models.CharField
        a variable to store revenue as an string
    sales_number : models.IntegerField
        a variable to store numbers of sales as an integer
    user : models.ForeignKey
        a variable to store the Foriegn Key of User Table

    Methods
    -------
    __str__(self)
        returns the string
    """

    date = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=50, default='')
    revenue = models.CharField(max_length=50, default='')
    sales_number = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns an string

        Parameters
        ----------
        self : Country Class Object
            an instance of Country class

        Returns
        ------
        String
            a customized string
        """

        return ("{} - {} ({})".format(self.product, self.sales_number, self.user.email))