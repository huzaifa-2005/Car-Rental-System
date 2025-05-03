from django.contrib import admin
from .models import CustomUser, Car, Rental, Transaction,ContactMessage

admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(Rental)
admin.site.register(Transaction)
admin.site.register(ContactMessage)

