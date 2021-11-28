from django.urls import path
from .views import base_views, comment_views
from . import views

app_name = 'polls'
urlpatterns = [
    # base_views.py
    # path('', base_views.index, name='index'),
    path('', base_views.IndexView.as_view(), name='index'),
    # path('<int:question_id>/', base_views.detail, name='detail'),
    path('<int:pk>', base_views.DetailView.as_view(), name='detail'),
    # path('<int:question_id>/results/', base_views.result, name='results'),
    path('<int:pk>/results/', base_views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', base_views.vote, name='vote'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
]
