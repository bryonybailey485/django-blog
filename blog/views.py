from django.shortcuts import render, get_object_or_404
from .models import Post, Status

def post_list(request):
    # Get published posts only
    published_status = Status.objects.filter(name__iexact='published').first()
    posts = Post.objects.filter(status=published_status).order_by('-published_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if post is published
    if not post.is_published():
        # If user is not admin, don't show unpublished posts
        if not request.user.is_staff:
            return render(request, 'blog/post_not_found.html')
    
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)
