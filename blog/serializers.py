from rest_framework import serializers
from blog.models import Post, Category, Comment
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        write_only=True,
        source='categories'
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content',
            'created_at', 'updated_at',
            'is_published',
            'categories',     
            'category_ids',
            'author'    
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'author']


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CommentSerializer(value, context=self.context)
        return serializer.data



class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.StringRelatedField(read_only=True)
    replies = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post','author', 'name', 'email', 'content', 'created_at', 'parent', 'replies']      
        read_only_fields = ['created_at', 'author']  

    def validate(self, data):
        parent = data.get('parent')
        post = data.get('post')

        if parent and parent.post != post:
            raise serializers.ValidationError("Parent comment must belong to same post")

        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user