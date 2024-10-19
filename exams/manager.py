from django.db import models


class QuestionManager(models.Manager):
    def correct_by_user(self, user):
        return self.filter(answer__choice__is_right=True, answer__session__user=user).distinct()

    def incorrect_by_user(self, user):
        return self.filter(answer__choice__is_right=False, answer__session__user=user).distinct()

    def skipped_by_user(self, user):
        answered_question_ids = self.filter(answer__session__user=user)\
                                    .values_list('pk', flat=True)
        return self.exclude(pk__in=answered_question_ids).distinct()
