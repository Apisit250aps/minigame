from django.contrib import admin
from .models import Topic, Question

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_desc", "created_at", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    date_hierarchy = "created_at"

    def short_desc(self, obj):
        if not obj.description:
            return "-"
        return (obj.description[:60] + "…") if len(obj.description) > 60 else obj.description
    short_desc.short_description = "Description"


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("question", "difficulty", "is_active", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_question",
        "topic",
        "difficulty",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "difficulty", "topic", "created_at")
    search_fields = ("question", "answer", "explanation", "topic__name")
    readonly_fields = ("id", "created_at", "updated_at")
    list_editable = ("is_active", "difficulty")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("topic",)

    def short_question(self, obj):
        return (obj.question[:80] + "…") if len(obj.question) > 80 else obj.question
    short_question.short_description = "Question"