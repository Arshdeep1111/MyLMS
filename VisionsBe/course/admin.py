from django.contrib import admin
from .models import *

# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model=Choice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]
    list_display = ['id', 'question', 'positive_marks', 'negative_marks']

class AssessmentInLine(admin.TabularInline):
    model = Assessment

class NoteInLine(admin.TabularInline):
    model = Note

class VideoInLine(admin.TabularInline):
    model = Video

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [AssessmentInLine, NoteInLine, VideoInLine]
    list_display = ['id', 'topic', 'description', 'is_preview']

class TeacherInLine(admin.TabularInline):
    model = Teacher

class TagInLine(admin.TabularInline):
    model = Tag

class PrerequisiteInLine(admin.TabularInline):
    model = Prerequisite

class LearningInLine(admin.TabularInline):
    model = Learning

class ReviewInLine(admin.TabularInline):
    model = Review

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [TagInLine, PrerequisiteInLine, LearningInLine, ReviewInLine, TeacherInLine]
    list_display = ['name', 'price', 'discount', 'is_active', 'language']

@admin.register(UserAssessment)
class UserAssessmentAdmin(admin.ModelAdmin):
    list_display=['pk']

admin.site.register(Wishlist)
admin.site.register(Favourite)
admin.site.register(My_course)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(UserProfile)


