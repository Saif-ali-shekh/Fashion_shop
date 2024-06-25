from rest_framework import serializers
from App_Models.models import *

class UserSignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )
    
    mobile = serializers.CharField(
        required=False,
        error_messages={
            'required': 'Mobile number is required.',
            'blank': 'Mobile number cannot be blank',
        }
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=False,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'email cannot be blank',
        }
    )
    
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters long.',
        },
        write_only=True,
        min_length=6  # Minimum length validation
    )
    confirm_password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Confirm Password is required.',
        },
        write_only=True
    )

    address = serializers.CharField(
        required=False,
        error_messages={
            'required': 'Address is required.',
        }
    )
    type = serializers.CharField(
        default='customer',
        read_only=True
    )
   

    class Meta:
        model = CustomBaseUser
        fields = ['name', 'email', 'address','mobile','type','confirm_password','password']

    def validate(self, data):
        mobile = data.get('mobile')
        if CustomBaseUser.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("This mobile number has already been registered.")
        if CustomBaseUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("This email has already been registered.")
        confirm_password = data.get('confirm_password')
        password = data.get('password')
        if password and confirm_password and confirm_password != password:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
       
        user_data = {
            'type': 'customer',
            'name': validated_data.get('name'),
            'mobile': str(validated_data.get('mobile')),
            'email': validated_data.get('email'),
            'address': validated_data.get('address'),
            
        }
        user = CustomBaseUser.objects.create(**user_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()
        return user



    
#-------------------   login 
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'Email cannot be blank',
        }
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Password is required.',
        },
        write_only=True
    )

    class Meta:
        fields = ['email', 'password']
############
class CustomBaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBaseUser
        fields = ['id', 'name', 'email', 'type', 'mobile', 'country', 'state', 'city', 'pincode', 'address', 'slug_field']
        

class UserAddSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = CustomBaseUser
        fields = ['name', 'email', 'mobile', 'address', 'type']

    def validate(self, data):
        # Additional validation as per your requirements
        return data

    def create(self, validated_data):
        # Create user based on validated data
        user_data = {
            'name': validated_data.get('name'),
            'email': validated_data.get('email'),
            'mobile': validated_data.get('mobile'),
            'address': validated_data.get('address'),
            'type': validated_data.get('type'),
        }
        print(user_data['mobile'])
        password = validated_data.get(user_data['mobile'])
        

        user = CustomBaseUser.objects.create_user(**user_data, password=password)
        if user.type=='customer':
            customer=Customer.objects.create(user=user)
        return user
##############
class DesignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignImage
        fields = ['id', 'image']
class DesignsSerializer(serializers.ModelSerializer):
    design_images = DesignImageSerializer(many=True, required=False)

    class Meta:
        model = Designs
        fields = ['id', 'design_name', 'design_images']

    def create(self, validated_data):
        design_images_data = validated_data.pop('design_images', [])
        design = Designs.objects.create(**validated_data)
        for image_data in design_images_data:
            DesignImage.objects.create(design_obj=design, **image_data)
        return design
    
###########show Images
class DesignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignImage
        fields = ['id', 'image']

class DesignsWithImagesSerializer(serializers.ModelSerializer):
    design_images = DesignImageSerializer(many=True, read_only=True)

    class Meta:
        model = Designs
        fields = ['id', 'design_name', 'design_images']