from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


# class PostListView(ListView):
#     template_name='blog/post_list.html'
#     context_object_name='posts'
#     queryset=Post.published.all()
#     paginate_by=3
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            # results = (
            #     Post.published.annotate(
            #         search=search_vector, rank=SearchRank(search_vector, search_query)
            #     )
            #     .filter(rank__gte=0.3)
            #     .order_by("-rank")
            # )

            results=Post.published.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.1).order_by('-similarity')
    return render(
        request, "blog/search.html", {"results": results, "form": form, "query": query}
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, status=Post.Status.PUBLISH, id=post_id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments:{cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request, "blog/share.html", {"form": form, "post": post, "sent": sent}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISH,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:2]
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If the page requested is out of range,return the last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post_list.html", {"posts": posts, "tag": tag})
