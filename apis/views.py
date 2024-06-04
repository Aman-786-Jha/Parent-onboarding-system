from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from onboarding_model.models import ParentOnboardingUser, Child, BlogCategory, Blog
from drf_yasg import openapi

class ParentOnboardingUserSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
         request_body=ParentOnboardingUserSerializer,
        responses={
            201: openapi.Response(description='Created', schema=ParentOnboardingUserSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error')
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
            500: 'Internal Server Error',
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

class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body= BlogSerializer,
        responses={
            201: openapi.Response(description='Created', schema=BlogSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
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
            201: openapi.Response(description='Created', schema=ChildSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
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
    @swagger_auto_schema(
        request_body=ChildSerializer,
        responses={
            201: openapi.Response(description='Created', schema=ChildSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
    )
    def put(self, request, child_id):
        try:
            child = get_object_or_404(Child, id=child_id)
            serializer = ChildSerializer(child, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Child updated successfully.',
                        'responseData': serializer.data,
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
            print("ChildUpdateView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    @swagger_auto_schema(
        responses={
            201: openapi.Response(description='Created', schema=ChildSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
    )

    def delete(self, request, child_id):
        try:
            child = get_object_or_404(Child, id=child_id)
            child.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Child deleted successfully.',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("ChildDeleteView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class BlogListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: 'OK',
            400: 'Bad Request',
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
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
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
    )
    def get(self, request, pk):
        try:
            blog = get_object_or_404(Blog, id=pk)
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
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
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
        request_body= ChildSerializer,
        responses={
            201: 'Created',
            400: 'Bad Request',
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                default='Bearer ',
                description='Token',
            ),
        ]
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
                    'responseMessage': 'Something went wrong!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    

    
