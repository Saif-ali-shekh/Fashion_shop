from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import *
from rest_framework_simplejwt.tokens import RefreshToken
from App_Models.models import *
from .serializers import *
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

class UserSignupView(APIView):
    # parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': "Account Created successfully",
                        'responseData': {
                            "full_name": user.name,
                            "email": user.email,
                            "userRole": user.type,
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1]}" for error in dict(e.detail).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                
                if CustomBaseUser.objects.filter(email=email).exists():
                    user = CustomBaseUser.objects.get(email=email)
                    
                    if user and user.check_password(password):
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        refresh_token = str(refresh)
                        user.is_active = True
                        user.save()
                        return Response(
                            {
                                'responseCode': status.HTTP_200_OK,
                                'responseMessage': "Login successful",
                                'responseData': {
                                    "full_name": user.name,
                                    "email": user.email,
                                    "userRole": user.type,
                                    'access_token': access_token,
                                    'refresh_token': refresh_token
                                }
                            },
                            status=status.HTTP_200_OK
                        )
                   
                    return Response(
                        {
                            'responseCode': status.HTTP_401_UNAUTHORIZED,
                            'responseMessage': "Invalid credentials",
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                return Response(
                        {
                            'responseCode': status.HTTP_401_UNAUTHORIZED,
                            'responseMessage': "User is not valid",
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )

        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(e.detail).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("login  Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


##############OWNER######################

class UserListView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            user =request.user
            if user and user.type !='Owner':
                return Response(
                {
                    'responseCode': status.HTTP_401_UNAUTHORIZED,
                    'responseMessage': 'you are not  authorized to access this api',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            users = CustomBaseUser.objects.all()
            serializer = CustomBaseUserSerializer(users, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': "Users retrieved successfully",
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(e.detail).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("UserListView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class UserAddView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerUser]  # Custom permission for owner

    def post(self, request):
        try:
            
            serializer = UserAddSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': "User added successfully",
                        'responseData': {
                            "full_name": user.name,
                            "email": user.email,
                            "userRole": user.type,
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(" Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

####### Add Designs


class AddDesignView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerUser]
    parser_classes = [MultiPartParser] 
    def post(self, request):
        try:
            serializer = DesignsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': "Design created successfully",
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("AddDesignView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
######
class DesignsWithImagesView(APIView):
    def get(self, request):
        designs = Designs.objects.all()
        serializer = DesignsWithImagesSerializer(designs, many=True)
        return Response(serializer.data)