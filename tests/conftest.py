import pytest
from pytest_factoryboy import register

from .fixtures.factories import (
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
register("user_factory", UserFactory)
register("category_factory", CategoryFactory)
register("exam_factory", ExamFactory)
register("subject_factory", SubjectFactory)
register("source_factory", SourceFactory)
register("question_factory", QuestionFactory)
register("choice_factory", ChoiceFactory)
register("issue_factory", IssueFactory)
register("session_factory", SessionFactory)
register("answer_factory", AnswerFactory)