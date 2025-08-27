from rest_framework import serializers
from .models import Topic, Question


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class QuestionSerializer(serializers.ModelSerializer):

    difficulty_display = serializers.CharField(
        source="get_difficulty_display", read_only=True
    )

    topic = TopicSerializer(read_only=True)

    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source="topic", write_only=True
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "question",
            "answer",
            "explanation",
            "difficulty",
            "difficulty_display",
            "topic",
            "topic_id",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):

        q = attrs.get("question") or getattr(self.instance, "question", "")
        if not (q and q.strip()):
            raise serializers.ValidationError({"question": "ห้ามเว้นว่างนะคะ"})
        return attrs


class PublicQuestionSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        exclude = ["answer"]
