# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Add models to interface."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm

from courses.models import Resource, Question
from scheduler import deadlineManager, inactivity_courses
from . import models
from .models import User


class UserAdmin(BaseUserAdmin):
    """Add moodle id to the User Admin interface."""

    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'password', 'moodle_id')


admin.site.register(User, UserAdmin)


def manual_inactivity(modeladmin, request, queryset):
    """Add an option to manually check the inactivity."""
    for query in queryset:
        inactivity_courses.create_job(query.courseId, query.inactivity_time)


manual_inactivity.short_description = "Perform inactivity check."


def manual_deadline(modeladmin, request, queryset):
    """Add an option to manually check the deadlines."""
    for query in queryset:
        deadlineManager.notify_about_upcoming_deadlines(86400, query.courseId)


manual_deadline.short_description = "Perform upcoming deadline check."


class ResourceInlineForm(ModelForm):
    """Create resource form."""

    # TODO maybe
    # def __init__(self, *args, **kwargs):
    #     """Sort the resources by name."""
    #     super(ResourceInlineForm, self).__init__(*args, **kwargs)
    #     # self.fields['parent'].queryset = Resource.objects.filter(parent_id__isnull=True)


class ResourceInline(admin.TabularInline):
    """Create the horizontal resource layout for the internal resource."""

    def get_queryset(self, request):
        """
        Overwrite the standard get_queryset function, to only select the resources that are internal.

        :param request: The get_queryset request.
        :return: All the resources that are internal.
        """
        qs = super(ResourceInline, self).get_queryset(request)
        return qs.filter(external=False)

    def has_change_permission(self, request, obj=None):
        """
        Overwrite the standard has_change_permission function, to make it read-only.

        :param request: The has_change_permission request.
        :param obj: The object.
        :return: False, everything here is read-only.
        """
        return False

    def has_add_permission(self, request, obj=None):
        """
        Overwrite the standard has_add_permission function, to remove add resource button.

        :param request: The has_add_permission request.
        :param obj: The object.
        :return: False, no objects should be added, since they are loaded from Moodle.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Overwrite the standard has_delete_permission function, to remove delete resource button.

        :param request: The has_delete_permission request.
        :param obj: The object.
        :return: False, nothing should be deleted from Mofa since it is loaded from Moodle.
        """
        return False

    exclude = ['external', 'external_id']
    ordering = ('target',)
    form = ResourceInlineForm
    model = Resource
    extra = 0
    verbose_name_plural = "Imported Resources (cannot be edited)"


class ResourceInlineExternal(admin.TabularInline):
    """Create the horizontal resource layout for external resource."""

    def get_queryset(self, request):
        """
        Overwrite the standard get_queryset function, to only select the resources that are external.

        :param request: The get_queryset request.
        :return: All the resources that are external.
        """
        qs = super(ResourceInlineExternal, self).get_queryset(request)
        return qs.filter(external=True)

    exclude = ['external', 'external_id']
    form = ResourceInlineForm
    model = Resource
    extra = 0
    verbose_name_plural = "External Resources (may be edited)"


class ResourceForm(ModelForm):
    """Create resource form and sort them alphabetically."""

    def __init__(self, *args, **kwargs):
        """Sort the resources by name."""
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['resources'].queryset = Resource.objects.order_by('name')
        self.fields['resources'].queryset = Resource.objects.filter(course_id=self.instance.course.id)

    class Meta:
        model = models.Quiz
        exclude = []


class QuestionInline(admin.TabularInline):
    """Create questions horizontal layout."""

    def has_add_permission(self, request, obj=None):
        """
        Overwrite the standard has_add_permission function, to remove add content button.

        :param request: The has_add_permission request.
        :param obj: The object.
        :return: False, no objects should be added, since they are loaded from Moodle.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Overwrite the standard has_delete_permission function, to remove delete content button.

        :param request: The has_delete_permission request.
        :param obj: The object.
        :return: False, nothing should be deleted from Mofa since it is loaded from Moodle.
        """
        return False

    fields = ('name', 'subjects', 'resources')
    model = Question
    extra = 0
    exclude = ('course', 'external_id')
    readonly_fields = ('name',)


class AssessmentAdmin(admin.ModelAdmin):
    """Abstract class that filter queryset and checks permissions."""

    def get_queryset(self, request):
        """Filter queryset to only show assessments the user has access to."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(course__in=request.user.courses.all())

    def has_view_or_change_permission(self, request, obj=None):
        """Restrict the user from viewing/changing assessments the user has access to."""
        if request.user.is_superuser:
            return True
        courses = request.user.courses.all()
        if obj is not None:
            return courses.filter(courseId=obj.course.courseId).exists()
        else:
            return True

    def has_add_permission(self, request):
        """
        Set add permission on false. Assessments are loaded from Moodle, should not be added manually.

        :param request: The add_permission request.
        :return: False, disable add permissions.
        """
        return False

    class Meta:
        abstract = True

    exclude = ['course', 'external_id']
    readonly_fields = ('name',)
    fields = ('name', 'subjects', 'contents')


@admin.decorators.register(models.Quiz)
class QuizAdmin(AssessmentAdmin):
    """Admin page for quizzes."""

    form = ResourceForm
    fields = ('name', 'course', 'subjects', 'resources')
    readonly_fields = ('name', 'course',)
    list_display = ('__str__', 'course',)
    filter_horizontal = ('resources',)
    inlines = [QuestionInline]

    class Media:
        """Include extra css."""

        css = {
            'all': ('css/inline_override.css',)
        }


@admin.decorators.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    """Whitelist the parameters shown in the admin panel. Add the manual actions."""

    list_display = ('name', 'courseId', 'inactivity', 'platform', 'deadline', 'warnings')
    actions = [manual_deadline, manual_inactivity]
    inlines = [ResourceInline, ResourceInlineExternal]
    readonly_fields = ('name', 'courseId')

    def delete_queryset(self, request, queryset):
        """
        Call delete on every course individually when deleting multiple courses.

        :param request: request
        :param queryset: all selected courses
        """
        for course in queryset:
            course.delete()
        super(CourseAdmin, self).delete_queryset(request, queryset)

    fieldsets = (
        (None, {
            'fields': ('name', 'platform', 'courseId')
        }),
        ('Inactivity', {
            'fields': ('inactivity', 'inactivity_time')
        }),
        ('Deadline', {
            'fields': ('deadline', 'hours_before')
        })
    )

    class Media:
        """Include extra css."""

        css = {
            'all': ('css/inline_override.css',)
        }

    def warnings(self, object):
        """
        Add warnings to user interface.

        At this moment a static warning. Should be changed to a warning when possible asynchronicity is detected in the
        future.
        :param object: A course ID.
        :return: The warning message.
        """
        # TODO.
        # return '⚠️ Warning: This course is not linked to an active {} course.'.format(object.platform)

    def has_view_or_change_permission(self, request, obj=None):
        """Restrict the user from viewing/changing courses the user has access to."""
        if request.user.is_superuser:
            return True
        courses = request.user.courses.all()
        if obj is not None:
            return courses.filter(courseId=obj.courseId).exists()
        else:
            return True

    def get_queryset(self, request):
        """Filter queryset to only show courses the user has access to."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(pk__in=request.user.courses.all())

    def has_add_permission(self, request):
        """
        Set add_permission on false. Courses are loaded from Moodle, should not be added manually.

        :param request: The add_permission request.
        :return: False, disable add permissions.
        """
        return False


@admin.decorators.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin page for subjects."""

    list_display = ('__str__', 'course',)
    filter_horizontal = ('resources',)


@admin.decorators.register(models.Assignment)
class AssignmentAdmin(AssessmentAdmin):
    """Admin page for assignment."""

    # readonly_fields = ('name', 'course')
    form = ResourceForm
    fields = ('name', 'course', 'subjects', 'resources')
    readonly_fields = ('name', 'course',)
    list_display = ('__str__', 'course',)
    filter_horizontal = ('resources',)


@admin.decorators.register(models.Choice)
class ChoiceAdmin(AssessmentAdmin):
    """Admin page for assignment."""

    form = ResourceForm
    fields = ('name', 'course', 'subjects', 'resources')
    readonly_fields = ('name', 'course',)
    list_display = ('__str__', 'course',)
    filter_horizontal = ('resources',)
