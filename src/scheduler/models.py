# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""Contains all database models."""
from django.db import models


class ProcessedStatement(models.Model):
    """Defines a processed statement."""

    statement_id = models.CharField(max_length=40, primary_key=True)

    class Meta:
        verbose_name = "processed statement"


class FailedStatement(models.Model):
    """Defines a failed statement."""

    statement = models.TextField()
    error = models.CharField(max_length=20)

    class Meta:
        verbose_name = "failed statement"


IGNORED_VERBS = {
    'http://id.tincanapi.com/verb/viewed',
    'http://adlnet.gov/expapi/verbs/answered'
}
