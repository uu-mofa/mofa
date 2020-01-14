# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""All the logic about giving feedback."""

from courses.models import Quiz, Resource, Question


def get_questions_feedback(params, question_feedback, questions):
    """
    Get the message that needs to be sent to student.

    :param params: Info about the attempt.
    :param question_feedback: Does it need receive feedback?
    :param questions: Questions and whether they are answered correctly or not.
    :return: Message that needs to be sent.
    """
    message = ''
    if question_feedback:
        if False in questions.values():
            feedback_link = get_question_feedback_link(questions)
            message = build_completed_questions_feedback(params['actor_name'], params['quiz_name'],
                                                         params['course_name'], params['score'] * 10,
                                                         feedback_link)
    return message


def get_quiz_feedback(params, action):
    """
    Quiz feedback that needs to be sent to the student.

    :param params: Info about the students attempt.
    :param action: The agents variables.
    :return: Message that needs to be sent to the Student.
    """
    threshold = action.threshold
    message = ''
    if params['score'] < threshold / 10:
        feedback = get_quiz_feedback_link(params['quiz_id'])
        message = build_completed_quiz_feedback(params['actor_name'], params['quiz_name'],
                                                params['course_name'], params['score'] * 10, feedback)
    return message


def get_quiz_feedback_link(quiz_id):
    """
    Make a feedback string for the completed quiz feedback based on the content or subject linked to the quiz.

    :param quiz_id: id from the quiz.
    :return: a string that contains the feedback.
    """
    resources = Resource.objects.filter(quiz__external_id=quiz_id)
    subject = Quiz.objects.filter(external_id=quiz_id)[0].subjects_id
    # if a quiz is linked to Content.
    if len(resources) != 0:
        name_content = resources[0].name
        target_content = resources[0].target
        link = f'<a href="{target_content}">{name_content}</a>'
    # if a quiz is linked to a Subject
    elif subject is not None:
        link = ""
        content_array = Resource.objects.filter(subject__id=subject)
        # if no Content is linked to the Subject
        if len(content_array) == 0:
            link = "the course resource"
        # if Content IS linked to the Subject
        else:
            for resources in content_array:
                link += '\r\n- <a href="{}">{}</a>'.format(resources.target, resources.name)
    # if no Content and no Subject is linked to a quiz
    else:
        link = "the course resource"

    return link


def get_question_feedback_link(questions):
    """
    Generate the link that is sent to the student.

    :param questions: Attempt's questions and whether they are correctly answered or not.
    :return: The message that needs to be sent, including HTML.
    """
    link = ['']
    for question in questions:
        # if question ID's value is false:
        if not questions[question]:
            # if wrongly answered question has content, get its name and target
            if not len(Question.objects.get(external_id=question).resources.values_list('name', flat=True)) == 0:
                target_content = Question.objects.get(
                    external_id=question).resources.values_list('target', flat=True)[0]
                name_content = Question.objects.get(external_id=question).resources.values_list('name', flat=True)[0]
                # if content is there, it always has a name. Check if it also has a target which can be linked to:
                if target_content is not None:
                    # If so, send a link to the target:
                    new_link = f'<p><a href="{target_content}">{name_content}</a></p>'
                else:
                    # Otherwise, just show the name:
                    new_link = f'<p> {name_content}</p>'
                if new_link not in link:
                    link.append(new_link)
            # If question has no content, check whether it has a subject and then do the same things as before:
            else:
                if not Question.objects.get(external_id=question).subjects is None:
                    subjects = Question.objects.get(external_id=question).subjects.resources.values_list('target',
                                                                                                         flat=True)
                    if not len(subjects) == 0:
                        for i in range(len(subjects)):
                            content_targets = subjects[i]
                            content_name = (
                                Question.objects.get(external_id=question).subjects.resources.values_list('name',
                                                                                                          flat=True)[
                                    i])
                            if content_targets is not None:
                                new_link = f'<p><a href="{content_targets}">{content_name}</a></p>'
                            else:
                                new_link = f'<p>{content_name}</p>'
                            if new_link not in link:
                                link.append(new_link)
    return ''.join(link)


def build_completed_quiz_feedback(actor_name, quiz_name, course_name, score, feedback):
    """
    Build the feedback when an user has completed the quiz and has failed the quiz.

    :param actor_name: name of the user that has completed the quiz.
    :param quiz_name: name of the quiz.
    :param course_name: name of the course.
    :param score: result of the user.
    :param feedback: string with the feedback.
    :return: string of the message.
    """
    message = f'Hi {actor_name},\n You have completed the quiz "{quiz_name}" for the course "{course_name}". ' \
              f'Your result was {score}, maybe you should look at: {feedback}'
    return message


def build_completed_questions_feedback(actor_name, quiz_name, course_name, score, feedback):
    """
    Build the feedback when an user has completed the quiz and has failed the quiz.

    :param actor_name: name of the user that has completed the quiz.
    :param quiz_name: name of the quiz.
    :param course_name: name of the course.
    :param score: result of the user.
    :param feedback: string with the feedback.
    :return: string of the message.
    """
    message = f'Hi {actor_name},\n You have completed the quiz "{quiz_name}" for the course "{course_name}". ' \
              f'Your result was {score}. For information about the topics of the questions you answered wrong' \
              f', please take a look at: {feedback}'
    return message
