from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from blog.models import Post, Category, Comment
from blog.serializers import PostSerializer, CategorySerializer, CommentSerializer, RegisterSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from blog.filters import PostFilter
from blog.pagination import CustomPagination
from blog.services import get_all_posts, soft_delete_post
from blog.permissions import IsOwnerOrReadOnly, IsCommentOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    # my-posts endpoint to get posts of the authenticated user
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    # comments endpoint to get comments of a specific post
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()   # related_name='comments'

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)  

    def get_queryset(self):
        return get_all_posts()
    
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        soft_delete_post(post)
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_200_OK
        )
        
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('post', 'author').prefetch_related('replies')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related('post', 'author').prefetch_related('replies')

        post_id = self.request.query_params.get('post')

        if post_id:
            return queryset.filter(post_id=post_id, parent=None)

        # Default: only top-level comments
        return queryset.filter(parent=None)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   

              


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.get(user=user)

        return Response({
            "message": "User registered successfully",
            "token": token.key
        }, status=201)