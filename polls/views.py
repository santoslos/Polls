from django.db.models import Q
from django.shortcuts import render
from django.views.generic.detail import DetailView
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .serializers import *
from .models import *


# Create your views here.


class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollListView(generics.ListAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollCreateView(generics.CreateAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class PollUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollListSerializer
    permission_classes = (permissions.IsAdminUser,)


class QuestionsCreateView(generics.CreateAPIView):
    serializer_class = QustionListSerializer
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class QuestionsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QustionListSerializer
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        polls = self.get_object().polls.all()
        for p in polls:
            print(p)
            obj = Poll.objects.get(pk=p.pk)
            if obj.time_start:
                raise serializers.ValidationError('Вопросы нельзе удалить, так как опрос уже начат')
            else:
                p.question_set.remove(self.get_object())
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChoiceCreateView(generics.CreateAPIView):
    serializer_class = ChoiceSerializerList
    queryset = Choice.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class ChoiceUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializerList
    queryset = Choice.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class AnswerUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class QuestionAnswerListView(generics.ListAPIView):
    serializer_class = PollsDetailUserSerializer

    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        queryset = Poll.objects.exclude(~Q(question__answer__user=pk))
        return queryset
