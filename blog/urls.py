from .views import post_list,post_detail,PostListView,post_share
from django.urls import path

app_name="blog"
urlpatterns=[
    # path("",PostListView.as_view(),name="post_list"),
    path("",post_list,name="post_list"),
    path("<slug:tag_slug>/",post_list,name="post_list_by_tag"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/",post_detail,name="post_detail"),
    path("<int:post_id>/share_post/",post_share,name="post_share"),
]
