from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

#
from .serializers import QuestionSerializer, PublicQuestionSerializer, TopicSerializer
from .models import Question, Topic

# Create your views here.


def index(request):
    return render(request, "index.html")


@api_view(["GET"])
@permission_classes([AllowAny])
def quests_list(request):
    questions = Question.objects.all()
    topics = Topic.objects.all()

    public_questions_serializer = PublicQuestionSerializer(many=True)
    questions_serializer = QuestionSerializer(questions, many=True)
    topic_serializer = TopicSerializer(topics, many=True)

    return Response(
        {
            "public_questions": public_questions_serializer.data,
            "questions": questions_serializer.data,
            "topics": topic_serializer.data,
        }
    )
