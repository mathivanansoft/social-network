from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics, exceptions
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.mixins import ListModelMixin
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

from .models import CustomUser
from .serializers import FindUsersSerializer, CustomUserSerializer, CustomUserReadSerializer
from utils.response import generate_response 

class ListUserAPIView(generics.ListAPIView):
    serializer_class = FindUsersSerializer

    def get_queryset(self):
        try:
            query = self.request.query_params.get("search")
            if query:
                validate_email(query)
                self.valid_email = True
                queryset = CustomUser.objects.filter(username__iexact=query).first()
            else:
                raise exceptions.ParseError("search required in query param")

        except ValidationError:
            queryset = CustomUser.objects.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            ).order_by('id')
        return queryset

    def get(self, request, *args, **kwargs):
        self.valid_email = False
        queryset = self.get_queryset()
        if self.valid_email:
            serializer_class = self.get_serializer_class()
            if queryset:
                serializer = serializer_class(queryset)
                data = serializer.data
                return generate_response(data=data)
            else:
                data = None
                raise exceptions.NotFound()
        else:
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

class SignupAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(CustomUserReadSerializer(user).data, status=status.HTTP_200_OK)
