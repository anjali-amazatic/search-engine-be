from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import (
    RegisterSerializer, SearchSerializer, ViewAllSerializer, SaveDataSerializer)
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.pagination import CustomPagination
from user.models import Search
from rest_framework.viewsets import ModelViewSet


class LoginApi(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]

    @action(methods=('POST',), detail=False, url_path='login')
    def login_api(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        _, token = AuthToken.objects.create(user)
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password
            },
            'token': token
        })

    @action(methods=['GET'], detail=False, url_path='get-user-data')
    def get_user_data(self, request):
        users = request.user

        if users.is_authenticated:
            return Response({
                'user_info': {
                            'id': users.id,
                            'username': users.username,
                            'email': users.email
                            },
            })
        return Response({'error': 'User not authenticated'}, status=400)

    # creating new user
    @action(methods=['POST'], detail=False, url_path='signup')
    def register_api(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
            'token': token
        })


class SearchedData(APIView):
    # permission_classes = [IsAuthenticated]
    ordering_fields = ['created_at']

    def post(self, request):
        data = request.data
        users = User.objects.get(username=request.user)
        data['user'] = request.user.id
        serializer = SearchSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data)


class ViewAll(generics.ListAPIView):
    pagination_class = CustomPagination
    # ordering = ['created_at']

    def list(self, requset):
        data = requset.data
        queryset = Search.objects.all().order_by('-created_at')
        data['user'] = requset.user.id
        serializer = ViewAllSerializer(queryset, many=True)
        return Response(serializer.data)

class SaveData(APIView):

    def post(self, request):
        data = request.data
        # users = User.objects.get(username=request.user)
        data['user'] = request.user.id
        serializer = SaveDataSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data)