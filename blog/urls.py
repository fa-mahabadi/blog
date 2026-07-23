from .views import post_list, post_detail, post_share,post_search
from django.urls import path
from blog.feeds import LastestPostFeed


app_name = "blog"
urlpatterns = [
    # path("",PostListView.as_view(),name="post_list"),
    path("", post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="post_detail"
    ),
    path("<int:post_id>/share_post/", post_share, name="post_share"),
    path("feed/", LastestPostFeed(), name="post_feed"),
    path("search/",post_search,name="post_search"),

]
