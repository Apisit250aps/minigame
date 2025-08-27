import uuid
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # insert ครั้งแรก
    updated_at = models.DateTimeField(auto_now=True)  # อัปเดตทุกครั้ง

    def __str__(self):
        return self.name


class Question(models.Model):
    class Difficulty(models.IntegerChoices):
        EASY = (1,)
        MEDIUM = (2,)
        HARD = (3,)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.TextField()  # คำถาม
    answer = models.TextField()  # เฉลย
    explanation = models.TextField(null=True, blank=True)  # อธิบายคำตอบ
    difficulty = models.PositiveSmallIntegerField(
        choices=Difficulty.choices, default=Difficulty.EASY
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    # เทียบกับ CURRENT_TIMESTAMP และ ON UPDATE CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)  # insert ครั้งแรก
    updated_at = models.DateTimeField(auto_now=True)  # อัปเดตทุกครั้ง

    def __str__(self):
        return (self.question[:60] + "…") if len(self.question) > 60 else self.question
