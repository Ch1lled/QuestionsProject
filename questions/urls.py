from django.urls import include , path
from . import views


urlpatterns = [
    path('test/', views.test, name='test'), 
    path('', views.main, name='main'), 
    path('register/', views.register, name='register'), 
    path('questions/', views.questions, name='questions'),
    path('questions/<int:question_id>/', views.question, name='question'), 
    path('questions/asking/', views.asking, name='asking'), 
    path('questions/<int:question_id>/replying/', views.replying, name='replying'), 
    path('questions/<int:question_id>/question_like/', views.question_like, name='question_like'), 
    path('questions/<int:question_id>/question_dislike/', views.question_dislike, name='question_dislike'),
    path('questions/<int:question_id>/<int:answer_id>/answer_like/', views.answer_like, name='answer_like'),
    path('questions/<int:question_id>/<int:answer_id>/answer_dislike/', views.answer_dislike, name='answer_dislike'), 
    path('questions/tags/', views.tags_list, name='tags_list'), 
    path('questions/tag/<str:slug>', views.tag, name='tag'), 
    #path('questions/<int:question_id>/add_tag/', views.add_tag, name='add_tag')
]