import pytest
from pytest_factoryboy import register

from tests.fixtures.factories import (
    UserFactory,
    CategoryFactory,
    ExamFactory,
    SubjectFactory,
    SourceFactory,
    QuestionFactory,
    ChoiceFactory,
    IssueFactory,
    SessionFactory,
    AnswerFactory,
)

# Register factories as fixtures
register(UserFactory)
register(CategoryFactory)
register(ExamFactory)
register(SubjectFactory)
register(SourceFactory)
register(QuestionFactory)
register(ChoiceFactory)
register(IssueFactory)
register(SessionFactory)
register(AnswerFactory)