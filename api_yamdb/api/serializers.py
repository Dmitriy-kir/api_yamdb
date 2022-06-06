import os
import sys
from datetime import date

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from users.models import User

sys.path.append(os.path.abspath('..'))

BLOCK_USERNAME = ('me',)

SCORE_RANGE = 10


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'] in BLOCK_USERNAME:
            raise serializers.ValidationError(
                f"Нельзя использовать имя - {data['username']}"
            )
        return data

    class Meta:
        fields = (
            'username',
            'email'
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(required=True,)

    class Meta:
        fields = (
            'username',
            'confirmation_code'
        )


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = SlugRelatedField(required=True)

    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Genres


class TitlesPostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)
    genre = SlugRelatedField(
        required=True,
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )
    category = SlugRelatedField(
        required=True,
        slug_field='slug',
        many=False,
        queryset=Categories.objects.all()
    )
    rating = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        return Reviews.obj.all().aggregate(Avg('score'))['score__avg']

    def validate(self, data):
        if data['year'] > date.today():
            raise serializers.ValidationError(
                'Некорректная дата'
            )
        return data

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Titles


class TitlesGetSerializer(serializers.ModelSerializer):
    titles_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)
    genre = SlugRelatedField(
        required=True,
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )
    category = SlugRelatedField(
        required=True,
        slug_field='slug',
        many=False,
        queryset=Categories.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    def get_avg_rating(self, obj):
        return Reviews.obj.all().aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    title_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(
        required=True,
        max_value=10,
        min_value=0
    )
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate_score(self, data):
        if data['score'] not in range(SCORE_RANGE):
            raise serializers.ValidationError(
                'Оценка некорректна, выберите число от 1 до 10'
            )
        return data

    def validate_author(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['request'].title_id
            if Reviews.objects.filter(
                    user=user,
                    title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на произведение'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comments


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        unique_together = ('username', 'email')


class UserMySelfSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        read_only_fields = 'role'
