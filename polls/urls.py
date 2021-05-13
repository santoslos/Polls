from django.urls import path
from .views import PollListView, PollDetailView, PollCreateView, PollUpdateDeleteView, QuestionsCreateView, \
    QuestionsUpdateDeleteView, ChoiceCreateView, AnswerCreateView, AnswerListView, AnswerUpdateDeleteView, \
    QuestionAnswerListView,ChoiceUpdateDeleteView

urlpatterns = [
    path('polls/', PollListView.as_view(), name='all'),
    path('polls/detail/<int:pk>/questions/', PollDetailView.as_view(), name='poll'),
    path('polls/create/', PollCreateView.as_view(), name='create'),
    path('polls/detail/<int:pk>/', PollUpdateDeleteView.as_view(), name='UpDel'),
    path('questions/create', QuestionsCreateView.as_view(), name='ques_create'),
    path('questions/<int:pk>', QuestionsUpdateDeleteView.as_view(), name='quesUbDel'),
    path('choice/create', ChoiceCreateView.as_view(), name='choice_create'),
    path('choice/detail/<int:pk>/', ChoiceUpdateDeleteView.as_view(), name='choice_create'),
    path('answer/create', AnswerCreateView.as_view(), name='answer_create'),
    path('answer/', AnswerListView.as_view(), name='answer_create'),
    path('answer/<int:pk>', AnswerUpdateDeleteView.as_view(), name='answer_update'),
    path('polls/questions/answer/<int:pk>', QuestionAnswerListView.as_view(), name='ques_answ'),

]
