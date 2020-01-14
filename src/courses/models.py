# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Create the models for the Django admin interface here."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from scheduler.main_scheduler import main_scheduler

EVENT_CHOICES = [
    ('http://id.tincanapi.com/verb/viewed', 'Viewed'),
    ('http://adlnet.gov/expapi/verbs/answered', 'Quiz Question Answered'),
    ('http://activitystrea.ms/schema/1.0/create', 'New Activity Created'),
]


class Course(models.Model):
    """Defines a course."""

    name = models.CharField(max_length=50, help_text='The course name.', editable=False)
    platform = models.CharField(max_length=50, choices=[('Moodle', 'Moodle'), ('Blackboard', 'Blackboard')],
                                default="Moodle")
    courseId = models.IntegerField(help_text='The course ID of the course on the LMS.',
                                   verbose_name="Course ID", editable=False, unique=True)
    inactivity = models.BooleanField('Enable inactivity check',
                                     help_text="Sends a message when a user hasn't logged in for a certain time.",
                                     default=False)
    inactivity_time = models.IntegerField("Days inactive", default=7,
                                          help_text="A message is send to students who have been "
                                                    "inactive for the specified number of days.")
    deadline = models.BooleanField('Enable deadline check',
                                   help_text="Sends a message to students certain time "
                                             "before a deadline when they haven't submitted anything.",
                                   default=False)
    hours_before = models.IntegerField("Hours before early deadline warning", default=24,
                                       help_text="How many hours before the deadline "
                                                 "needs the student to be notified?")

    class Meta:
        indexes = [
            models.Index(fields=['courseId'])
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """On save, if deadline or inactivity is checked, add the jobs to the scheduler."""
        self.__delete_jobs__()
        if self.deadline:
            main_scheduler.add_deadline_early_notification(self.courseId, self.hours_before * 3600)
            main_scheduler.add_deadline_late_notification(self.courseId)
        if self.inactivity:
            main_scheduler.add_inactivity_notification(self.courseId, self.inactivity_time)
        super(Course, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """On delete, delete the scheduled job."""
        success = True
        self.__delete_jobs__()
        assistant_list = list(self.newactivitycreated_set.all()) + list(self.quizcompletedfeedback_set.all())
        for assistant in assistant_list:
            if not assistant.delete():
                success = False
        super(Course, self).delete(*args, **kwargs)
        return success

    def __delete_jobs__(self):
        if str(self.courseId) + "late" in main_scheduler.jobs:
            main_scheduler.remove_job(self.courseId, "late")
            main_scheduler.remove_job(self.courseId, "early")
        if str(self.courseId) + "inactive" in main_scheduler.jobs:
            main_scheduler.remove_job(self.courseId, "inactive")


TYPE_CHOICES = (
    ('book', 'Book'),
    ('chapter', 'Chapter'),
    ('lesson', 'Lesson'),
    ('url', 'Website'),
    ('resource', 'File'),
    ('folder', 'Folder'),
    ('page', 'Page'),
    ('wiki', 'Wiki'),

)


class Resource(models.Model):
    """
    Defines resource.

    Resource has a name and is linked to a course. Has one of the predefined types and has a target.
    Chapters can have a book as parent.
    External is a bool that defines if it is external resource, internal course resource cannot be edited.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, help_text="What is this resource called?")
    type = models.CharField(max_length=256, choices=TYPE_CHOICES, help_text="What kind of resource is this?")
    target = models.URLField(verbose_name="Link", null=True, blank=True, max_length=256,
                             help_text="The link to the resource")
    external = models.BooleanField(editable=False, default=True)
    external_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # NB: Targets are not unique, two courses could have the same external resource, say, a website.
        unique_together = ('course', 'target')
        indexes = [
            models.Index(fields=['target'])
        ]


class Subject(models.Model):
    """
    Defines a subject.

    A subject has a name and is linked to a course and contains (multiple) resource objects.
    """

    name = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    resources = models.ManyToManyField(Resource, blank=True)

    def __str__(self):
        return self.name


class Assessment(models.Model):
    """
    Defines all standard fields for assessments in Moodle.

    An assessment is always linked to a course and has a name. This information is loaded from Moodle.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=256)
    subjects = models.ForeignKey(Subject, blank=True, on_delete=models.CASCADE, null=True)
    resources = models.ManyToManyField(Resource, blank=True)
    external_id = models.IntegerField()

    class Meta:
        abstract = True
        unique_together = ('course', 'external_id')
        indexes = [
            models.Index(fields=['external_id'])
        ]

    def __str__(self):
        return self.name


class Quiz(Assessment):
    """A quiz is a type of assessment."""

    class Meta:
        verbose_name_plural = "quizzes"


class Choice(Assessment):
    """A choice is a type of assessment."""


class Question(Assessment):
    """A Quiz has multiple questions."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Assignment(Assessment):
    """An assignment is a type of assessment."""

    pass


class User(AbstractUser):
    """Add a Moodle ID to the user model."""

    moodle_id = models.IntegerField(blank=True, null=True)
    courses = models.ManyToManyField(Course)
