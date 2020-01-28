# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""This file contains all parsers that parse information from Moodle API calls."""


def parse_enrolled_students(enrolled_users):
    """
    Parse the statements containing all enrolled students of a course.

    :param enrolled_users: A json statement, received as response on a Moodle call.
    :type enrolled_users: list(dict(str, int))
    :return: A list of the ids of the enrolled students.
    :rtype: list(str)
    """
    students = []
    for student_info in enrolled_users:
        students.append(str(student_info['id']))
    return students


def parse_course_info(course):
    """
    Parse information of a course that is retrieved from Moodle.

    :param course: A json statement, received as response on a Moodle call.
    :type course: dict(str, list(dict(str, int)))
    :return: The name of a course.
    :rtype: str
    """
    course_name = course['courses'][0]['fullname']
    return course_name


def parse_courses(courses):
    """
    Parse information of all courses that are retrieved from Moodle.

    :param courses: Statements for all courses.
    :type courses: list(dict(str, int))
    :return: A dictionary containing the names and ids of all courses.
    :rtype: list(dict(str, int))
    """
    courses = courses[:]
    del courses[0]
    course_info = [{"courseId": course['id'], "name": course['fullname']} for course in courses]
    return course_info


def parse_assignment_list(assignments):
    """
    Parse all assignments of a course from a statement received from Moodle.

    :param assignments: A statement containing all assignments of a course.
    :type assignments: dict(str, list(dict(str, int)))
    :return: A dictionary of all assignments of a course.
    :rtype: list(dict(str, int))
    """
    temp_assign = assignments['courses'][0]['assignments']
    return temp_assign


def parse_single_assignment(assignment):
    """
    Parse the useful information from a single assignment.

    :param assignment: All information of a single assignment.
    :type assignment: dict(str, str)
    :return: The id, due_date and name of an assignment.
    :rtype: tuple(int, int, str)
    """
    assignment_id = assignment['cmid']
    name = assignment['name']
    due_date = assignment['duedate']
    return assignment_id, due_date, name


def parse_get_course_contents(course_contents, courseId):
    """
    Extract used course contents for a specific course.

    Extract only needed course contents. Ignore contents of module type forum, lti, feedback, workshop, data, chat,
    survey or glossary. Return the other contents in a dictionary.

    :param course_contents: All contents of a course.
    :type course_contents: list(dict(str, int))
    :param courseId: The id of the course the contents are from.
    :type courseId: int
    :return: A list of dictionaries. Each dictionary contains a course id, module name, target, type and external id.
    :rtype: list(dict(str, int))
    """
    content_list = []
    for section in course_contents:
        for module in section['modules']:
            if module['modname'] == 'forum' or module['modname'] == 'lti' or module['modname'] == 'feedback' or \
                    module['modname'] == 'workshop' or module['modname'] == 'data' or module['modname'] == 'chat' or \
                    module['modname'] == 'survey' or module['modname'] == 'glossary':
                continue
            if module['modname'] == 'book':
                for content in module['contents'][1:]:
                    url = "{}&chapterid={}".format(module['url'], content["filepath"][1:-1])
                    content_list.append(
                        {'course_id': courseId, 'name': content["content"], 'target': url,
                         'type': "chapter", 'external_id': int(content["filepath"][1:-1])}
                    )

            content_list.append(
                {'course_id': courseId, 'name': module['name'], 'target': module['url'], 'type': module['modname'],
                 'external_id': int(module['id'])}
            )

    return content_list


def parse_get_teachers(courses):
    """
    Parse the teacher information received from Moodle.

    :param courses: All information about all courses in Moodle.
    :type courses: list(dict(str, int))
    :return: A list of dictionaries containing all user information and the course they are teacher from.
    :rtype: dict(int, dict(str, str))
    """
    teachers_list = {}
    for course in courses:
        for user in course['users']:
            roles = []
            for role in user['roles']:
                roles.append(role['shortname'])
            if user['id'] in teachers_list:
                teachers_list[user['id']]['courses'].update({course['courseid']: roles})
            else:
                teachers_list[user['id']] = {"username": user['username'], "id": user['id'],
                                             "firstname": user['firstname'],
                                             "lastname": user["lastname"], "email": user['email'],
                                             "courses": {course['courseid']: roles}
                                             }

    return teachers_list
