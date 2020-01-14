# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Add models to interface."""
from django.contrib import admin, messages

from assistants import learning_locker
from . import models


class AssistantAdmin(admin.ModelAdmin):
    """Admin class to add warnings to all Assistants."""

    list_display = ('course', 'warnings')
    exclude = ('forwarder_id',)

    @staticmethod
    def warnings(obj):
        """Add warnings to an assistant when there is no statement forwarder of the assistant in LL."""
        if learning_locker.check_statement_forwarder(obj.forwarder_id):
            return ''
        else:
            return '⚠️This assistant has no statement forwarder in Learning Locker. ' \
                   'Save the assistant again to create a new statement forwarder. ⚠️'

    @staticmethod
    def has_error(obj):
        """Check whether or not the obj contains a broken statement forwarder."""
        if obj is not None:
            return not learning_locker.check_statement_forwarder(obj.forwarder_id)
        else:
            return False

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """Override the render_change_form to add a warning when a statement forwarder is broken."""
        if self.has_error(obj):
            self.message_user(request=request, level=messages.WARNING,
                              message='This assistant has no statement forwarder in Learning Locker. '
                                      'Save the assistant again to create a new statement forwarder.')
        return super(AssistantAdmin, self).render_change_form(request, context, add=add, change=not add, obj=obj,
                                                              form_url=form_url)


@admin.decorators.register(models.NewActivityCreated)
class NewActivityCreatedAdmin(AssistantAdmin):
    """Add new activity to admin interface."""

    def delete_queryset(self, request, queryset):
        """Override bulk delete function. Also deletes the LL Forwarders."""
        for query in queryset:
            models.NewActivityCreated.delete(query)


@admin.decorators.register(models.QuizCompletedFeedback)
class QuizCompletedFeedbackAdmin(AssistantAdmin):
    """Add feedback for quiz to admin interface."""

    def delete_queryset(self, request, queryset):
        """Override bulk delete function. Also deletes the LL Forwarders."""
        for query in queryset:
            models.QuizCompletedFeedback.delete(query)
