from rest_framework import serializers
from django.contrib.auth import authenticate
from onboarding_model.models import ParentOnboardingUser, Child, BlogCategory, Blog
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator, MaxValueValidator


class ParentOnboardingUserSerializer(serializers.ModelSerializer):
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
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.',
            'blank': 'Password cannot be blank',
        }
    )

    confirm_password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        error_messages={
            'required': 'Confirm Password is required.',
            'blank': 'Confirm Password cannot be blank',
        }
    )

    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Name is required.',
            'blank': 'Name cannot be blank',
        }
    )

    contact_details = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Contact details are required.',
            'blank': 'Contact details cannot be blank',
        }
    )

    address = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Address is required.',
            'blank': 'Address cannot be blank',
        }
    )

    class Meta:
        model = ParentOnboardingUser
        fields = ['id', 'user_type', 'experience_type', 'name', 'email', 'password', 'confirm_password', 'contact_details', 'address']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if ParentOnboardingUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email has already been registered.")

        if password != confirm_password:
            raise serializers.ValidationError("The password fields do not match.")

        return data

    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        contact_details = validated_data.get('contact_details')
        address = validated_data.get('address')
        user_type = validated_data.get('user_type')
        experience_type = validated_data.get('experience_type')

        user = ParentOnboardingUser.objects.create_user(
            email=email,
            name=name,
            password=password,
            contact_details=contact_details,
            address=address,
            user_type=user_type,
            experience_type=experience_type
        )

        return user

class ChildSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Name is required.',
            'blank': 'Name cannot be blank',
        }
    )

    age_in_months = serializers.IntegerField(
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        error_messages={
            'required': 'Age in months is required.',
            'invalid': 'Enter a valid age in months.',
            'min_value': 'Age cannot be less than 0 months.',
            'max_value': 'Age cannot be more than 240 months.'
        }
    )

    gender = serializers.ChoiceField(
        choices=Child.gender_choices,
        required=True,
        error_messages={
            'required': 'Gender is required.',
            'invalid_choice': 'Enter a valid gender.'
        }
    )

    class Meta:
        model = Child
        fields = ['id', 'parent', 'name', 'age_in_months', 'gender']

class BlogCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Category name is required.',
            'blank': 'Category name cannot be blank',
        }
    )

    class Meta:
        model = BlogCategory
        fields = ['id', 'name']

class BlogSerializer(serializers.ModelSerializer):
    categories = BlogCategorySerializer(many=True, read_only=True)
    parent_types = ParentOnboardingUserSerializer(many=True, read_only=True)
    title = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Title is required.',
            'blank': 'Title cannot be blank',
        }
    )
    
    content = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Content is required.',
            'blank': 'Content cannot be blank',
        }
    )

    age_group_start = serializers.IntegerField(
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        error_messages={
            'required': 'Starting age group is required.',
            'invalid': 'Enter a valid starting age group in months.',
            'min_value': 'Age group start cannot be less than 0 months.',
            'max_value': 'Age group start cannot be more than 240 months.'
        }
    )

    age_group_end = serializers.IntegerField(
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        error_messages={
            'required': 'Ending age group is required.',
            'invalid': 'Enter a valid ending age group in months.',
            'min_value': 'Age group end cannot be less than 0 months.',
            'max_value': 'Age group end cannot be more than 240 months.'
        }
    )

    gender_specific = serializers.ChoiceField(
        choices=Child.gender_choices,
        required=False,
        allow_null=True,
        error_messages={
            'invalid_choice': 'Enter a valid gender.'
        }
    )

    geolocation = serializers.CharField(
        required=False,
        allow_blank=True,
        error_messages={
            'blank': 'Geolocation cannot be blank if provided.',
        }
    )

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'categories', 'parent_types', 'age_group_start', 'age_group_end', 'gender_specific', 'geolocation']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email and password are required.')
