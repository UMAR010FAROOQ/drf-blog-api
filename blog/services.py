from blog.models import Post, Category, Comment\


def get_all_posts():
    return (
        Post.objects
        .filter(is_deleted=False)
        .only('id', 'title', 'slug', 'created_at', 'is_published')
        .prefetch_related('categories')
    )


def soft_delete_post(post):
    post.is_deleted = True
    post.save()
    return post

# def soft_delete_post(post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#         post.is_deleted = True
#         post.save()
#         return True
#     except Post.DoesNotExist:
#         return False