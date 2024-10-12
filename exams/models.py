from datetime import datetime, timezone
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.apps import apps
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


class Subject(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
    marking_users = models.ManyToManyField(User, blank=True,
                                           related_name="marked_questions")
    created_at = models.DateTimeField(auto_now_add=True)

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
    number_of_questions = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(25)])
    subjects = models.ManyToManyField(Subject, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"Answer for {self.question} in Session #{self.session.pk}"
