from django.shortcuts import render, get_object_or_404, redirect 
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category,Comment

def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
   
    posts_list = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
   
    if category_id:
        posts_list = posts_list.filter(category_id=category_id)


    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'posts': posts, 
        'query': query,
        'categories': categories,
        'selected_category': category_id
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')

        if name and email and body:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                body=body
            )
            return redirect('post_detail', pk=post.pk)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })