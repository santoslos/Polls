from rest_framework import serializers

from .models import *


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user


class ChoiceSerializerList(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(queryset=Question.objects.exclude(question_category='TX'),
                                            slug_field='pk')
    title = serializers.CharField(max_length=100)

    class Meta:
        model = Choice
        fields = ['pk', 'title', 'question']

    def create(self, validated_data):
        if validated_data['question'].question_category == 'TX':
            raise serializers.ValidationError('Для этого вопроса нельзя создать вариант ответа')
        return Choice.objects.create(**validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['title']


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')
    question_category = ChoiceField(choices=CATEGORY)

    class Meta:
        model = Choice
        fields = ['pk', 'title', 'question_category', 'choices']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set', read_only=True)

    class Meta:
        model = Poll
        fields = ['pk', 'title', 'description', 'questions']


class AnswerSerializer(serializers.Serializer):
    user = serializers.IntegerField(default=CurrentUserDefault())
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='pk')
    choices = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='pk',
                                           allow_null=True)
    choices_text = serializers.CharField(max_length=250, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = ['pk', 'user', 'question', 'choices', 'choices_text']

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):

        ques = Question.objects.get(pk=attrs['question'].pk)
        question_category = ques.question_category
        choices = ques.choice_set.all()
        ans = Answer.objects.filter(question=attrs['question'].pk, user=attrs['user'])
        if question_category == 'CN' or question_category == 'MC':
            attrs['choices_text'] = None
            if attrs['choices'] not in choices:
                raise serializers.ValidationError('Этого варианта ответа нет в вопросе')

        if question_category == 'TX' or question_category == 'CN':
            if ans:
                raise serializers.ValidationError('У Этого вопроса один ответ')
            if question_category == 'TX':
                if attrs['choices'] and not attrs['choices_text']:
                    raise serializers.ValidationError('У этого вопроса  нет варианта ответа ')
                elif not attrs['choices'] and not attrs['choices_text']:
                    attrs['choices_text'] = 'Нет ответа'
                else:
                    attrs['choices'] = None
        elif question_category == 'MC':
            ans = Answer.objects.filter(question=attrs['question'].pk, user=attrs['user'], choices=attrs['choices'])
            if ans:
                raise serializers.ValidationError('Вы уже выбрали этот вариант ответа')

        return attrs


class QustionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'question_category', 'polls']

    def create(self, validated_data):
        polls = validated_data['polls']
        for p in polls:
            print(p)
            obj = Poll.objects.get(pk=p.pk)
            if obj.time_start:
                raise serializers.ValidationError('Вопросы нельзя создать, так как опрос уже начат')
        pol = validated_data.pop('polls')
        questions = Question.objects.create(**validated_data)
        questions.polls.set(pol)
        return questions

    def update(self, instance, validated_data):

        polls = instance.polls.all()
        for p in polls:
            print(p)
            obj = Poll.objects.get(pk=p.pk)
            if obj.time_start:
                raise serializers.ValidationError('Вопросы нельзя обновить, так как опрос уже начат')

        pol = validated_data.pop('polls')
        for p in pol:
            print(p)
            obj = Poll.objects.get(pk=p.pk)
            if obj.time_start:
                raise serializers.ValidationError('Вопросы нельзя обновить, так как опрос уже начат')
        for key, value in validated_data.items():
            setattr(instance, key, value)
            print(key)
        instance.save()
        return instance


class AnswerserQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer()

    class Meta:
        model = Answer
        fields = ['choices', 'choices_text']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField('get_answers')

    def get_answers(self, question):
        user = self.context.get('request').parser_context['kwargs']['pk']
        answer = Answer.objects.filter(user=user, question=question)
        serializers = AnswerserQuestionSerializer(instance=answer, many=True)
        return serializers.data

    class Meta:
        model = Question
        fields = ['title', 'answer']


class PollsDetailUserSerializer(serializers.ModelSerializer):
    questions = QuestionAnswerSerializer(many=True, read_only=True, source='question_set')

    class Meta:
        model = Poll
        fields = ['title', 'questions']


class Test(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField('get_answers')

    def get_answers(self, question):
        user = self.context.get('request').parser_context['kwargs']['pk']
        answer = Answer.objects.filter(user=user, question=question)
        serializers = AnswerserQuestionSerializer(instance=answer, many=True)
        return serializers.data

    class Meta:
        model = Question
        fields = ['title', 'answer']
