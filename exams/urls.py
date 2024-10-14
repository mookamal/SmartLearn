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
    # urls for ajax
    path("ajax/get-question-count/",
         views.get_question_count, name="get_question_count"),
    path("ajax/create_session", views.ajax_create_session,
         name="ajax_create_session"),
]
