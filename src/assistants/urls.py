# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

from django.urls import path

from . import views

# Add your urls here
urlpatterns = [
    path('api/new_activity_notification/<int:action_id>/', views.new_activity_notification,
         name='new_activity_notification'),
    path('api/sync_agent/', views.sync_agent_execute, name='sync_agent'),
    path('api/quiz_completed_feedback/<int:action_id>/', views.quiz_completed_feedback, name='quiz_completed_feedback')
]
