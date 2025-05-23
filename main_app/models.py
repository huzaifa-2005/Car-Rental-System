from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime 
# MinValueValidator--Used to make sure numeric fields (like balance) are not negative

# __str__ is a Special Python method that defines the string representation of an object

'''Here in Django, by ORM (Object-Relational Mapping), it is meant that is a technique
        that Django uses to interact with your database,  
        allowing you to work with your database using Python objects rather than writing raw 
        SQL queries. '''

''' Here in django, Abstract base classes serve by allowing us to 
put some common information into a number of other models. '''

'''Abstract classes in Django focus on preventing table creation and allow sharing common fields--as done in this case with created_at field.'''
''' Meta class is like a settings panel or configuration handler specifically for each model. 
It's where we tell Django special instructions about how to treat the entire model in the database and throughout the framework.  ''' 

''' "Meta" is not a keyword but its a conventional name to represent the metadata of the model.
Its purpose is to give you a place to specify model-wide settings 
without cluttering up the main model definition with non-field related configurations. '''

# This is our abstract class that we have defined
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    # The abstract = True in Meta tells Django not to create a database table--keeping the model abstract.    


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0.0)]
    )
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
    
    def add_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self.save()
        return True
    
    def has_sufficient_balance(self, amount):
        return self.balance >= amount


class Car(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    brand = models.CharField(max_length=100)
    seating_capacity = models.PositiveIntegerField(null=False, blank=False)
    rent_per_day = models.PositiveIntegerField(null=False, blank=False)
    model_year = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/', default='media/car_images/default.jpg')

    def __str__(self):
        return f"{self.name} - {self.brand}"
    
    def is_available(self):
        return self.available
    
    def mark_unavailable(self):
        self.available = False
        self.save()
        
    def mark_available(self):
        self.available = True
        self.save()


#  Rental inherits created_at from abstract class
# This keeps track of which user rented which car, for how many days, and at what cost.
class Rental(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rentals')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    returned_early = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.start_date} to {self.end_date})"
    
    def calculate_days(self):
        delta = self.end_date - self.start_date
        return delta.days
    
    def calculate_cost(self):
        days = self.calculate_days()
        return days * self.car.rent_per_day
    # since we can't predict the future use, we always include the argument *args, **kwargs
    # to allow for any additional arguments that might be passed inside the save() method.
    # This method is called when the object is saved to the database.

    ''' we are setting values inside the view and then tweaking one value (e.g. total_cost ) 
    inside custom save present in the model if incase total_cost is not set in the view
    and then the Parent save handles the actual database write for all fields '''
    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.calculate_cost()
        super().save(*args, **kwargs)
    
    @classmethod
    # This method belongs to the class itself (not an instance) 
    # and can be called without creating an instance of the class.
    # It checks for rentals that should be returned today and marks them as inactive.
    # It also marks the car as available.
    # This method can be called as Rental.check_returns()
    # cls parameter is a convention (like self for instance methods) that allows 
    # the method to access and modify class-level attributes
    # and perform operations on the entire model (like querying the database).
    # cls = Rental (the class itself)
    def check_returns(cls):
        now = timezone.now()

        
        # in Django you cannot use the simple Python <= operator inside a filter() call
        # Django ORM does not parse native Python comparison operators (<, <=, etc.) in queries.
        #  Instead, Django uses "field lookups"
        # "field lookups" are special keywords connected with __ (double underscore) to perform comparisons in SQL.
        # __lte is lookup type for "less than or equal to"
        completed_rentals = cls.objects.filter(end_date__lte=now, is_active=True)
        for rental in completed_rentals:
            rental.is_active = False
            rental.save()
            rental.car.mark_available()


#  Transaction  inherits created_at from abstract class
class Transaction(TimeStampedModel):
    TRANSACTION_TYPES = (
        ('ADD', 'Add Money'),
        ('PAYMENT', 'Rental Payment'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ${self.amount}"


#  ContactMessage  inherits created_at from abstract class
class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Message from {self.name}"
