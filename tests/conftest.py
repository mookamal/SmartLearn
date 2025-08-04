import pytest
from pytest_factoryboy import register
from plan.models import SubscriptionPlan
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

@pytest.fixture(autouse=True)
def create_default_free_plan(db):
    SubscriptionPlan.objects.create(name="FREE", sessions_per_month=10, price=0, description="Free plan")

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