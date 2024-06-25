import graphene
from graphene import Int,Field
from graphene_django import DjangoObjectType
from App_Models.models import *
from graphql import GraphQLError

        
class CustomBaseUserType(DjangoObjectType):
    class Meta:
        model =CustomBaseUser
class CustomerType(DjangoObjectType):
    class Meta:
        model =Customer
class DesignsType(DjangoObjectType):
    class Meta:
        model =Designs
class ThreadsProductsType(DjangoObjectType):
    class Meta:
        model =ThreadsProducts
class ProductImageType(DjangoObjectType):
    class Meta:
        model =ProductImage
class DesignImageType(DjangoObjectType):
    class Meta:
        model =DesignImage

        
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi! this is graphql start with docker 123")
    All_User =graphene.List(CustomBaseUserType)
    All_Customer=graphene.List(CustomerType)
    All_Designs =graphene.List(DesignsType)
    All_Products =graphene.List(ThreadsProductsType)
    All_ProductImages =graphene.List(ProductImageType)
    All_DesignImages =graphene.List(DesignImageType)
    ####targrt by id 
    # User_ID =graphene.Field(CustomBaseUserType, id=graphene.Int(), slug=graphene.String())
    # user = graphene.Field(CustomBaseUserType, search=graphene.String(required=True))
    user = graphene.Field(CustomBaseUserType, id=graphene.Int(), slug=graphene.String())
    Customer_ID = graphene.Field(CustomerType, Customer_ID=Int(required=True))
    Design_ID = graphene.Field(DesignsType, Design_ID=Int(required=True))
    Product_ID = graphene.Field(ThreadsProductsType, Product_ID=Int(required=True))
    ProductImage_ID = graphene.Field(ProductImageType, ProductImage_ID=Int(required=True))
    DesignImage_ID = graphene.Field(DesignImageType, DesignImage_ID=Int(required=True))
    
    
    
    
    def resolve_All_User(self, request):
         return CustomBaseUser.objects.all()
    def resolve_All_Customer(self, request):
         return Customer.objects.all()
    def resolve_All_Designs(self, request):
         return Designs.objects.all()
    def resolve_All_Products(self, request):
         return ThreadsProducts.objects.all()
    def resolve_All_ProductImages(self, request):
         return ProductImage.objects.all()
    def resolve_All_DesignImages(self, request):
         return DesignImage.objects.all() 
     #####by id 
    # def resolve_User_ID(self, request, id=None, slug=None):
    #     try:
    #         # if not isinstance(User_ID, int):
    #         #     raise GraphQLError("Invalid ID: ID must be an integer.")
    #         # user=CustomBaseUser.objects.get(id=User_ID) 
    #         # return user
    #         if id is not None:
    #             try:
    #                 return CustomBaseUser.objects.get(pk=id)
    #             except CustomBaseUser.DoesNotExist:
    #                 return None
    #         elif slug is not None:
    #             try:
    #                 return CustomBaseUser.objects.get(slug_field=slug)
    #             except CustomBaseUser.DoesNotExist:
    #                 return None
    #         else:
    #             raise Exception("You must provide either an 'id' or a 'slug'")
    #     except Exception as e:
    #         raise  GraphQLError(f"user not found")
    
    # def resolve_user(self, info, search):
    #     print(search.isdigit())
    #     if search.isdigit():
    #         # Search by id
    #         try:
    #             return CustomBaseUser.objects.get(pk=int(search))
    #         except CustomBaseUser.DoesNotExist:
    #             return None
    #     else: 
    #         # Search by slug
    #         try:
    #             return CustomBaseUser.objects.get(slug_field=search)
    #         except CustomBaseUser.DoesNotExist:
    #             return None
    def resolve_user(self, info, id=None, slug=None):
        # if id is not None and slug is not None:
        #     raise GraphQLError("You must provide either 'id' or 'slug', not both.")
        if id is not None:
            try:
                return CustomBaseUser.objects.get(pk=id)
            except CustomBaseUser.DoesNotExist:
                raise GraphQLError(f"User with ID {id} not found")
        if slug is not None:
            try:
                return CustomBaseUser.objects.get(slug_field=slug)
            except CustomBaseUser.DoesNotExist:
                raise GraphQLError(f"User with slug {slug} not found")
        raise GraphQLError("You must provide either an 'id' or a 'slug'")

    def resolve_Customer_ID(self, info, Customer_ID):
        if not isinstance(Customer_ID, int):
            raise GraphQLError("Invalid ID: ID must be an integer.")
        try:
            return Customer.objects.get(id=Customer_ID)
        except Customer.DoesNotExist:
            raise GraphQLError(f"customer_id {Customer_ID} not found")
    
    def resolve_Design_ID(self, info, Design_ID):
        if not isinstance(Design_ID, int):
            raise GraphQLError("Invalid ID: ID must be an integer.")
        try:
            return Designs.objects.get(id=Design_ID)
        except Designs.DoesNotExist:
            raise GraphQLError(f"design_id {Design_ID} not found")
    
    def resolve_Product_ID(self, info, Product_ID):
        if not isinstance(Product_ID, int):
            raise GraphQLError("Invalid ID: ID must be an integer.")
        try:
            return ThreadsProducts.objects.get(id=Product_ID)
        except ThreadsProducts.DoesNotExist:
            raise GraphQLError(f"product_id {Product_ID} not found")
    
    def resolve_ProductImage_ID(self, info, ProductImage_ID):
        if not isinstance(ProductImage_ID, int):
            raise GraphQLError("Invalid ID: ID must be an integer.")
        try:
            return ProductImage.objects.get(id=ProductImage_ID)
        except ProductImage.DoesNotExist:
            raise GraphQLError(f"product_image_id {ProductImage_ID} not found")
    
    def resolve_DesignImage_ID(self, info, DesignImage_ID):
        if not isinstance(DesignImage_ID, int):
            raise GraphQLError("Invalid ID: ID must be an integer.")
        try:
            return DesignImage.objects.get(id=DesignImage_ID)
        except DesignImage.DoesNotExist:
            raise GraphQLError(f"design_image_id {DesignImage_ID} not found")

         

schema = graphene.Schema(query=Query)
