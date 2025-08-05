# This file is part of SmartLearn by Mohamed Kamal (github.com/mookamal) – Licensed under the MIT License
from datetime import datetime
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.apps import apps
from .manager import QuestionManager
# Create your models here.


class Source(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True)
    parent_source = models.ForeignKey('self', null=True, blank=True,
                                      related_name="children",
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_questions(self):
        # Dynamically load the Question model
        Question = apps.get_model('exams', 'Question')
        return Question.objects.filter(sources=self)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to="category_images", blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        related_name="children",
                                        on_delete=models.SET_NULL,
                                        default=None, limit_choices_to={"parent_category__isnull": True})
    is_listed = models.BooleanField("This category is listed upon showing categories and on the sidebar",
                                    default=True, blank=True)

    def __str__(self):
        return self.name

    def total_questions(self):
        # Dynamically load the Question model
        Question = apps.get_model('exams', 'Question')
        return Question.objects.filter(exam__category=self).count()

    def total_exams(self):
        # Dynamically load the Exam model
        Exam = apps.get_model('exams', 'Exam')
        return Exam.objects.filter(category=self, is_visible=True).count()


class Exam(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='exams',
                                 null=True,
                                 on_delete=models.SET_NULL, limit_choices_to={"parent_category__isnull": False})
    is_visible = models.BooleanField(default=True)
    description = CKEditor5Field(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_subjects(self):
        Subject = apps.get_model('exams', 'Subject')
        return Subject.objects.filter(question__exam=self).distinct()

    def get_questions(self):
        Question = apps.get_model('exams', 'Question')
        return Question.objects.filter(exam=self, is_approved=True)

    def get_sources(self):
        questions = self.get_questions()
        Source = apps.get_model('exams', 'Source')
        sources = Source.objects.filter(question__in=questions).distinct()
        return sources


class Subject(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # get Questions
    def get_questions(self):
        Question = apps.get_model('exams', 'Question')
        return Question.objects.filter(subject=self)


class Question(models.Model):
    sources = models.ManyToManyField(Source, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    issues = models.ManyToManyField('Issue', blank=True)
    text = models.TextField()
    figure = models.ImageField(upload_to="question_images",
                               blank=True)
    explanation = models.TextField(default="", blank=True)
    explanation_figure = models.ImageField(upload_to="explanation_images",
                                           blank=True)
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateField(blank=True, null=True)
    reference = models.TextField(default="", blank=True)
    labs = models.ManyToManyField('TestCategory', blank=True)
    marking_users = models.ManyToManyField(User, blank=True,
                                           related_name="marked_questions")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def save(self, *args, **kwargs):
        if self.is_approved and not self.approval_date:
            self.approval_date = datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Question #{self.text[:50]}"


class Choice(models.Model):
    text = models.CharField(max_length=255)
    is_right = models.BooleanField("Right answer?", default=False)
    question = models.ForeignKey(
        Question,  null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


session_mode_choices = (
    ('EXPLAINED', 'Explained'),
    ('UNEXPLAINED', 'Unexplained'),
    ('SOLVED', 'Solved'),
    ('INCOMPLETE', 'Incomplete'),
)


class Session(models.Model):
    session_mode = models.CharField(
        max_length=20, choices=session_mode_choices, default='EXPLAINED')
    number_of_questions = models.PositiveIntegerField(null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_order = models.JSONField(default=list)
    current_question_index = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    unused_question_count = models.PositiveIntegerField(default=0)
    # answer counts
    correct_answer_count = models.PositiveIntegerField(default=0)
    incorrect_answer_count = models.PositiveIntegerField(default=0)
    skipped_answer_count = models.PositiveIntegerField(default=0)

    def update_answer_counts(self):
        correct_count = self.questions.filter(
            answer__choice__is_right=True, answer__session=self).count() or 0
        incorrect_count = self.questions.filter(
            answer__choice__is_right=False, answer__session=self).count() or 0
        self.correct_answer_count = correct_count
        self.incorrect_answer_count = incorrect_count
        self.update_skipped_answer_count()
        self.save()

    def update_skipped_answer_count(self):
        total_questions = self.number_of_questions or self.questions.count()
        answered_questions = self.correct_answer_count + self.incorrect_answer_count
        self.skipped_answer_count = max(
            0, total_questions - answered_questions - self.unused_question_count)

        if self.skipped_answer_count < 0:
            self.skipped_answer_count = 0

        self.save()

    def is_session_completed(self):
        total_questions = self.number_of_questions or self.questions.count()
        Answer = apps.get_model('exams', 'Answer')
        answered_questions = Answer.objects.filter(session=self).count()
        return answered_questions >= total_questions

    def mark_as_completed(self):
        if self.is_session_completed():
            self.completed = True
            self.save()

    def __str__(self):
        return f"Session #{self.pk}"


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, null=True,
                               on_delete=models.CASCADE)
    is_first = models.BooleanField("Is this the first time this question was answered by the user?",
                                   blank=True, default=False)
    is_correct = models.BooleanField(
        "Is this the correct answer?", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "question")

    def save(self, *args, **kwargs):
        if Answer.objects.filter(session=self.session, question=self.question).exists():
            self.is_first = True
        else:
            self.is_first = False

        if self.choice:
            self.is_correct = self.choice.is_right
        super().save(*args, **kwargs)
        self.session.update_answer_counts()

    def __str__(self):
        return f"Answer for {self.question} in Session #{self.session.pk}"


class TestCategory(models.Model):
    """
    Model representing the main category for a group of tests.
    """
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class TestRow(models.Model):
    """
    Model representing a row within a category, containing three fields:
    1. Test name
    2. Reference range
    3. SI reference intervals
    """
    category = models.ForeignKey(
        TestCategory, on_delete=models.CASCADE, related_name="rows")
    test_name = models.CharField(max_length=255)
    reference_range = models.CharField(max_length=100)
    test_result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.test_name} - {self.reference_range} - {self.test_result}"
