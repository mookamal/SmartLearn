# This file is part of SmartLearn by Mohamed Kamal (github.com/mookamal) – Licensed under the MIT License
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("category/<str:slug>/", views.show_category, name="show_category"),
    path("category/<str:slug>/<int:sub_category_id>/",
         views.show_exams_by_category, name="show_exams_by_category"),
    path("category/<str:slug>/<int:sub_category_id>/<int:exam_id>/",
         views.create_session, name="create_session"),
    # session paths
    path("session/<int:session_id>/", views.show_session, name="show_session"),
    path("session/<int:session_id>/results/",
         views.session_results, name="session_results"),
    path("session/my_sessions/", views.my_sessions, name="my_sessions"),
    # performance
    path("performance/", views.performance, name="performance"),
    # urls for ajax
    path("ajax/get-question-count/",
         views.get_question_count, name="get_question_count"),
    path("ajax/create_session", views.ajax_create_session,
         name="ajax_create_session"),
    path("ajax/answer/", views.answer, name="answer"),
    path("ajax/navigate-question-index/",
         views.navigate_question_index, name="navigate_question_index"),
    path("ajax/finish_session/", views.finish_session, name="finish_session"),
    path("ajax/re_examine/", views.re_examine, name="re_examine"),
    path("ajax/delete-session/", views.delete_session, name="delete_session"),
    path("ajax/re-examine-by-exam/",
         views.re_examine_by_exam, name="re_examine_by_exam"),
    path("ajax/report-issue/", views.report_issue, name="report_issue"),
    path("ajax/mark-question/", views.mark_question, name="mark_question"),
    path("ajax/set_question_order/",
         views.set_question_order, name="set_question_order"),
]
