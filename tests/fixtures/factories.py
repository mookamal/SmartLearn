import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from exams.models import (
    Category,
    Exam,
    Subject,
    Question,
    Choice,
    Source,
    Session,
    Answer,
    Issue,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class ExamFactory(DjangoModelFactory):
    class Meta:
        model = Exam

    name = factory.Faker("sentence")
    category = factory.SubFactory(CategoryFactory)


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker("word")


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source

    name = factory.Faker("word")
    category = factory.SubFactory(CategoryFactory)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.Faker("paragraph")
    subject = factory.SubFactory(SubjectFactory)
    exam = factory.SubFactory(ExamFactory)

    @factory.post_generation
    def sources(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for source in extracted:
                self.sources.add(source)


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    text = factory.Faker("sentence")
    question = factory.SubFactory(QuestionFactory)
    is_right = False


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")


class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session

    user = factory.SubFactory(UserFactory)
    exam = factory.SubFactory(ExamFactory)
    number_of_questions = 10


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    session = factory.SubFactory(SessionFactory)
    question = factory.SubFactory(QuestionFactory)
    choice = factory.SubFactory(ChoiceFactory)
