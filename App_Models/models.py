from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomBaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomBaseUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )

    type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.PositiveBigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    slug_field = models.SlugField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomBaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.slug_field:
            base_slug = slugify(self.name) if self.name else slugify(self.email)
            base_slug =base_slug.lower()
            num = 1
            while CustomBaseUser.objects.filter(slug_field=base_slug).exists():
                base_slug = f"{base_slug}{num}"
                num += 1
            self.slug_field = base_slug
        super().save(*args, **kwargs)
            
            
class Customer(models.Model):
    user = models.ForeignKey(CustomBaseUser, related_name="customers", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

class Designs(models.Model):
    design_name = models.CharField(max_length=50, blank=True, null=True)

class ThreadsProducts(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)


class DesignImage(models.Model):
    Design_obj = models.ForeignKey('Designs', related_name='design_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='design_images', null=True, blank=True)

    def __str__(self):
        return f"Design Image {self.id}"

class ProductImage(models.Model):
    product_obj = models.ForeignKey('ThreadsProducts', related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return f"Product Image {self.id}"

