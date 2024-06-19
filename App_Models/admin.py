from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomBaseUser)
admin.site.register(Customer)
admin.site.register(Designs)
admin.site.register(ThreadsProducts)
admin.site.register(DesignImage)
admin.site.register(ProductImage)


