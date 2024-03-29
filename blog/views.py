from django.shortcuts import redirect, render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail

class PostListView(ListView):
    template_name = 'blog/post/list.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    


# Create your views here.
# added new changes
def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = Paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'page':page,'posts':posts})
    
    
def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post, slug=post, status = 'published',publish__year = year,publish__month = month, publish__day = day)
    
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form})
    
    
def post_create(request):
    post = get_object_or_404(Post)
    if request.method=="POST":
        if form.is_valid():
            form.post = post
            form.save()
            form.save()
            return redirect('/mysite')
    else:
        form = Post()
        
        return render(request,'blog/post/create.html')

    

    
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent=False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'sabariask1307@gmail.com',[cd['to']])
            sent=True
            
    else:
        form = EmailPostForm()
            
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})




