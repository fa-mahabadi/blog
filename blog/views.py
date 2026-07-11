from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import EmptyPage, Paginator,PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm

class PostListView(ListView):
    template_name='blog/post_list.html'
    context_object_name='posts'
    queryset=Post.published.all()
    paginate_by=3


def post_share(request,post_id):
    post=get_object_or_404(Post,status=Post.Status.PUBLISH,id=post_id)
    sent=False
    if request.method=="POST":
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=(
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
                )
            message=(
                f"read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments:{cd['comments']}"
            )
            send_mail(subject=subject,message=message,from_email=None,recipient_list=[cd['to']])
            sent=True
           
    else:
        form=EmailPostForm()
    return render(request,'blog/share.html',{'form':form,'post':post,'sent':sent})
        






def post_list(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page',1)
    try:
        posts=paginator.page(page_number)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        # If the page requested is out of range,return the last page of results
        posts=paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,status=Post.Status.PUBLISH,publish__year=year,publish__month=month,publish__day=day,slug=post)
    return render(request,'blog/post_detail.html',{'post':post})