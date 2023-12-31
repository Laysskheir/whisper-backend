from store.models import Product
from .models import User
from rest_framework import serializers

# from store.serializers import OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    # orders = OrderSerializer(many=True, read_only=True)
    orders_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ("password",)

    def get_orders_count(self, obj):
        # orders is @property
        return obj.orders.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoggedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "bio",
        )


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, write_only=True, min_length=5)
    password2 = serializers.CharField(required=True, write_only=True, min_length=5)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords don't match")
        else:
            return data


class SearchUserSerializer(serializers.ModelSerializer):
    # orders_count = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "feature",
            "description",
            "price",
            "image",
            "category",
            "brand",
        )

    # def get_orders_count(self, obj):
    #      # orders is @property
    #     return obj.orders.count()




# ==================== AUTH ====================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # return a dictionary data with keys "access" and "refresh"
    pass


