from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    ParentOnboardingUserSerializer,
    ChildSerializer,
    BlogCategorySerializer,
    BlogSerializer,
    LoginSerializer,
)
from onboarding_model.models import ParentOnboardingUser, Child, BlogCategory, Blog

class ParentOnboardingUserSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
         request_body=ParentOnboardingUserSerializer,
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        try:
            serializer = ParentOnboardingUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'User created successfully.',
                        'responseData': serializer.data,
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
        except Exception as e:
            print("ParentOnboardingUserSignupView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: 'OK',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Login successful.',
                        'responseData': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                    'responseData': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal Server Error',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChildView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
         request_body=ChildSerializer,
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        try:
            serializer = ChildSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(parent=request.user)
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Child created successfully.',
                        'responseData': serializer.data,
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
        except Exception as e:
            print("ChildView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
         request_body=BlogSerializer,
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        try:
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Blog created successfully.',
                        'responseData': serializer.data,
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
        except Exception as e:
            print("BlogView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from django.shortcuts import get_object_or_404

class ChildDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, child_id):
        try:
            child = get_object_or_404(Child, id=child_id, parent=request.user)
            serializer = ChildSerializer(child)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Child details retrieved successfully.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("ChildDetailView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Child not found.',
                },
                status=status.HTTP_404_NOT_FOUND
            )

class BlogListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: 'OK',
            400: 'Bad Request',
        }
    )
    def get(self, request):
        try:
            blogs = Blog.objects.all()
            page = request.query_params.get('page', 1)
            paginator = Paginator(blogs, 10)

            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)

            serializer = BlogSerializer(blogs, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Blog list retrieved successfully.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("BlogListView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, blog_id):
        try:
            blog = get_object_or_404(Blog, id=blog_id)
            serializer = BlogSerializer(blog)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Blog details retrieved successfully.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("BlogDetailView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Blog not found.',
                },
                status=status.HTTP_404_NOT_FOUND
            )

from django.shortcuts import get_object_or_404

class BlogCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: 'OK',
            400: 'Bad Request',
        }
    )
    def get(self, request):
        try:
            categories = BlogCategory.objects.all()
            serializer = BlogCategorySerializer(categories, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Blog categories retrieved successfully.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("BlogCategoryListView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ChildCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        try:
            serializer = ChildSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(parent=request.user)
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Child created successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                    'responseData': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("ChildCreateView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                },
                status=status.HTTP_400_BAD_REQUEST
            )



