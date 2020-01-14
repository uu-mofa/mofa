# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""This file contains all parsers that parse information from moodle API calls."""


def parse_enrolled_students(enrolled_users):
    """
    Parse the JSON from Moodle of the enrolled students.

    :param enrolled_users: JSON (as retrieved from moodle.MoodleAPI.get_enrolled_users).
    :return: A list of the ids of the enrolled students.
    """
    students = []
    for student_info in enrolled_users:
        students.append(str(student_info['id']))
    return students


def parse_course_info(course):
    """
    Parse the JSON from Moodle of a single course.

    :param course: JSON
    :return: A string of the name of the course
    """
    return course['courses'][0]['fullname']


def parse_courses(courses):
    """Parse the JSON from Moodle of all the courses."""
    courses = courses[:]
    del courses[0]
    return [{"courseId": course['id'], "name": course['fullname']} for course in courses]


def parse_assignment_list(assignments):
    """
    Create a list of assignments from the JSON moodle provides.

    :param assignments: JSON from Moodle
    :return: List of assignments (including all its information)
    """
    return assignments['courses'][0]['assignments']


def parse_single_assignment(assignment):
    """
    Parse the useful information from a single course.

    :param assignment: all information of a single assignment
    :return: the id, due_date and name of an assignment
    """
    assignment_id = assignment['cmid']
    name = assignment['name']
    due_date = assignment['duedate']
    return assignment_id, due_date, name


def parse_get_course_contents(course_contents, courseId):
    """Extract all the course content for a course."""
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
    """Parse teachers information from Moodle."""
    teachers_list = {}
    for course in courses:
        for user in course['users']:
            if user['id'] in teachers_list:
                teachers_list[user['id']]['courses'].append(course['courseid'])
            else:
                teachers_list[user['id']] = {"username": user['username'], "id": user['id'],
                                             "firstname": user['firstname'],
                                             "lastname": user["lastname"], "email": user['email'],
                                             "courses": [course['courseid']]}

    return teachers_list
