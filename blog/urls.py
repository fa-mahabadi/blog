from .views import post_list,post_detail
from django.urls import path

app_name="blog"
urlpatterns=[
    path("",post_list,name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/",post_detail,name="post_detail")
]
