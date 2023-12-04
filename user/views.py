from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, decorators, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Product
from .pagination import CustomPagination
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.views import APIView

User = get_user_model()


def staff_required(view_func):
    def wrapped_view(view_instance, request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(view_instance, request, *args, **kwargs)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    return wrapped_view


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            # Allow unauthenticated access for user creation
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.serializer_class.Meta.model.objects.filter(
            is_active=True, pk=pk
        ).first()
        if user:
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, pk):
        user = self.get_object()
        serializer = UserCreateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staff_required
    def destroy(self, request, pk=None):
        user = self.get_object(pk=pk)
        user.is_active = False
        if user.is_active == False:
            user.save()
            return Response(
                {"message": "User deleted successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "User not deleted"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=["POST"], detail=True)
    def change_password(self, request, pk=None):
        user = self.get_object()
        password_serializer = ChangePasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data["password1"])  # hash
            user.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                password_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# ==================== AUTH ====================
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(username=username, password=password)  # validated instance

        if user:
            login_serializer = self.get_serializer(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response(
                    {
                        "access": login_serializer.validated_data["access"],
                        "refresh": login_serializer.validated_data["refresh"],
                        "user": user_serializer.data,
                        "message": "Login successful",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    login_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )



class UserLoggedDataView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            serializer = UserLoggedSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = request.user
            serializer = UserLoggedSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

class SearchProductView(APIView):
    def get(self, request):
        search_term = request.query_params.get("search", "")
        products = Product.objects.filter(
            Q(name__icontains=search_term)
            # Q(description__icontains=search_term)
        ).distinct()

        paginator = CustomPagination()
        results = paginator.paginate_queryset(products, request)

        serializer = SearchUserSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
