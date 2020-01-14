# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

test_parse_send_message_data = \
    {
        "activities": [
            "http://localhost:4000/course/view.php?id=2"
        ],
        "statement": {
            "actor": {
                "name": "Will Smith",
                "account": {
                    "name": "3"
                }
            },
            "context": {
                "platform": "Moodle"
            },
            "object": {
                "definition": {
                    "name": {
                        "en": "Test Test"
                    }
                }
            }
        }
    }
test_parse_viewed_courses_no_statements = \
    {
        "more": "",
        "statements": []
    }
test_parse_viewed_courses = \
    {
        "statements": [
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },

            {
                "actor": {
                    "account": {
                        "name": "5"
                    }
                }
            },

            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                },
            },
            {
                "actor": {
                    "account": {
                        "name": "3"
                    },
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "4"
                    },
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "4"
                    },
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            },
            {
                "actor": {
                    "account": {
                        "name": "2"
                    }
                }
            }
        ]
    }
test_parse_new_activity_created_data = \
    {
        "statement": {
            "context": {
                "extensions": {
                    "http://lrs.learninglocker.net/define/extensions/info": {
                        "http://moodle.org": "3.7.2 (Build: 20190909)",
                        "https://github.com/xAPI-vle/moodle-logstore_xapi": "v4.4.0",
                        "event_name": "\\core\\event\\course_module_created",
                        "event_function": "\\src\\transformer\\events\\core\\module_created"
                    }
                },
                "contextActivities": {
                    "grouping": [
                        {},
                        {
                            "id": "testtesttestid=1",
                            "definition": {
                                "name": {
                                    "en": "Test_Course"
                                }
                            }
                        }
                    ]
                }
            },
            "object": {
                "id": "http://localhost:4000/mod/quiz/view.php?id=38",
                "definition": {
                    "name": {
                        "en": "Test_Activity"
                    }
                }
            }
        }
    }
test_parse_enrolled_users = \
    [
        {
            "id": 2
        },
        {
            "id": 3
        },
        {
            "id": 4
        },
        {
            "id": 5
        }
    ]

test_parse_get_quizzes_by_course = \
    {
        "quizzes": [
            {
                "id": 1,
                "course": 2,
                "coursemodule": 6,
                "name": "Quiz 1",
                "intro": "<p>Quiz 1 description</p>"
            },
            {
                "id": 2,
                "course": 2,
                "coursemodule": 9,
                "name": "Quiz 2",
                "intro": "<p>Quiz 2 description</p>"
            }
        ],
        "warnings": []
    }

test_parse_get_books_by_course = \
    {
        "books": [
            {
                "id": 1,
                "coursemodule": 8,
                "course": 2,
                "name": "Book 1",
                "intro": "<p>Book 1 description</p>"
            },
            {
                "id": 2,
                "coursemodule": 12,
                "course": 2,
                "name": "Book 2",
                "intro": "<p>Book 2 description</p>"
            }
        ],
        "warnings": []
    }

test_parse_get_choices_by_course = \
    {
        "choices": [
            {
                "id": 2,
                "coursemodule": 10,
                "course": 2,
                "name": "Choice 1",
                "intro": "<p>Choice 1 description</p>"
            },
            {
                "id": 3,
                "coursemodule": 13,
                "course": 2,
                "name": "Choice 2",
                "intro": "<p>Choice 2 description</p>"
            }
        ],
        "warnings": []
    }
test_parse_get_courses = \
    [
        {
            "id": 1,
            "fullname": "Sting-IT Site",
        },
        {
            "id": 2,
            "fullname": "Testing Course",
        },
        {
            "id": 3,
            "fullname": "Inactivity Test Course",
        },
        {
            "id": 4,
            "fullname": "Deadline Test Course",
        }
    ]

test_parse_get_assignments = \
    {
        "courses": [
            {
                "assignments": [
                    {
                        "cmid": 7,
                        "course": 2,
                        "name": "Assignment 1",
                    },
                    {
                        "cmid": 11,
                        "course": 2,
                        "name": "Assignment 2",
                    }
                ]
            },
            {
                "assignments": [
                    {
                        "cmid": 4,
                        "course": 4,
                        "name": "Assignment 1",
                    }
                ]
            }
        ],
        "warnings": []
    }

test_get_courses_by_id = \
    {
        'courses': [
            {
                'id': 2,
                'fullname': 'BeginningCourse'
            }
        ]
    }

test_parse_get_course_contents = \
    [
        {
            "id": 1,
            "name": "General",
            "modules": [
                {
                    "id": 1,
                    "url": "http://localhost:4000/mod/forum/view.php?id=1",
                    "name": "Announcements",
                    "modname": "forum",
                }
            ]
        },
        {
            "id": 2,
            "name": "Topic 1",
            "modules": [
                {
                    "id": 6,
                    "url": "http://localhost:4000/mod/quiz/view.php?id=6",
                    "name": "Quiz 1",
                    "modname": "quiz",
                }
            ]
        },
        {
            "id": 3,
            "name": "Topic 2",
            "modules": [
                {
                    "id": 7,
                    "url": "http://localhost:4000/mod/assign/view.php?id=7",
                    "name": "Assignment 1",
                    "modname": "assign",
                },
                {
                    "id": 8,
                    "url": "http://localhost:4000/mod/book/view.php?id=8",
                    "name": "Book 1",
                    "modname": "book",
                    "contents": [
                        {
                            "type": "content",
                        },
                        {
                            "filepath": "/1/",
                            "content": "Chapter 1",
                        },
                        {
                            "filepath": "/2/",
                            "content": "Chapter 2",
                        },
                        {
                            "filepath": "/5/",
                            "content": "Chapter 3",
                        },
                        {
                            "filepath": "/9/",
                            "content": "Chapter 4",
                        },
                        {
                            "filepath": "/10/",
                            "content": "Subchapter",
                        }
                    ]
                },
                {
                    "id": 11,
                    "url": "http://localhost:4000/mod/assign/view.php?id=11",
                    "name": "Assignment 2",
                    "modname": "assign",
                }
            ]
        },
        {
            "id": 4,
            "name": "Topic 3",
            "modules": [
                {
                    "id": 10,
                    "url": "http://localhost:4000/mod/choice/view.php?id=10",
                    "name": "Choice 1",
                    "modname": "choice",
                },
                {
                    "id": 13,
                    "url": "http://localhost:4000/mod/choice/view.php?id=13",
                    "name": "Choice 2",
                    "modname": "choice",
                }
            ]
        },
        {
            "id": 5,
            "name": "Topic 4",
            "modules": [
                {
                    "id": 12,
                    "url": "http://localhost:4000/mod/book/view.php?id=12",
                    "name": "Book 2",
                    "modname": "book",
                    "contents": [
                        {
                            "type": "content",
                            "content": "[]",
                        }
                    ],
                },
                {
                    "id": 16,
                    "url": "http://localhost:4000/mod/resource/view.php?id=16",
                    "name": "File 1",
                    "modname": "resource",
                },
                {
                    "id": 17,
                    "url": "http://localhost:4000/mod/url/view.php?id=17",
                    "name": "URL 1",
                    "modname": "url",
                },
                {
                    "id": 18,
                    "url": "http://localhost:4000/mod/folder/view.php?id=18",
                    "name": "Folder 4",
                    "modname": "folder",
                },
                {
                    "id": 19,
                    "url": "http://localhost:4000/mod/page/view.php?id=19",
                    "name": "Page 4",
                    "modname": "page",
                }
            ]
        }
    ]

test_parse_get_course_contents_result = \
    [
        {'course_id': 1, 'name': 'Quiz 1',
         'type': 'quiz',
         'target': 'http://localhost:4000/mod/quiz/view.php?id=6', 'external_id': 6},
        {'course_id': 1, 'name': 'Assignment 1',
         'type': 'assign',
         'target': 'http://localhost:4000/mod/assign/view.php?id=7', 'external_id': 7},
        {'course_id': 1, 'name': 'Chapter 1',
         'type': 'chapter',
         'target': 'http://localhost:4000/mod/book/view.php?id=8&chapterid=1', 'external_id': 1},
        {'course_id': 1, 'name': 'Chapter 2',
         'type': 'chapter',
         'target': 'http://localhost:4000/mod/book/view.php?id=8&chapterid=2', 'external_id': 2},
        {'course_id': 1, 'name': 'Chapter 3',
         'type': 'chapter',
         'target': 'http://localhost:4000/mod/book/view.php?id=8&chapterid=5', 'external_id': 5},
        {'course_id': 1, 'name': 'Chapter 4',
         'type': 'chapter',
         'target': 'http://localhost:4000/mod/book/view.php?id=8&chapterid=9', 'external_id': 9},
        {'course_id': 1, 'name': 'Subchapter',
         'type': 'chapter',
         'target': 'http://localhost:4000/mod/book/view.php?id=8&chapterid=10', 'external_id': 10},
        {'course_id': 1, 'name': 'Book 1',
         'type': 'book',
         'target': 'http://localhost:4000/mod/book/view.php?id=8', 'external_id': 8},
        {'course_id': 1, 'name': 'Assignment 2',
         'type': 'assign',
         'target': 'http://localhost:4000/mod/assign/view.php?id=11', 'external_id': 11},
        {'course_id': 1, 'name': 'Choice 1',
         'type': 'choice',
         'target': 'http://localhost:4000/mod/choice/view.php?id=10', 'external_id': 10},
        {'course_id': 1, 'name': 'Choice 2',
         'type': 'choice',
         'target': 'http://localhost:4000/mod/choice/view.php?id=13', 'external_id': 13},
        {'course_id': 1, 'name': 'Book 2',
         'type': 'book',
         'target': 'http://localhost:4000/mod/book/view.php?id=12', 'external_id': 12},
        {'course_id': 1, 'name': 'File 1',
         'type': 'resource',
         'target': 'http://localhost:4000/mod/resource/view.php?id=16', 'external_id': 16},
        {'course_id': 1, 'name': 'URL 1',
         'type': 'url',
         'target': 'http://localhost:4000/mod/url/view.php?id=17', 'external_id': 17},
        {'course_id': 1, 'name': 'Folder 4',
         'type': 'folder',
         'target': 'http://localhost:4000/mod/folder/view.php?id=18', 'external_id': 18},
        {'course_id': 1, 'name': 'Page 4',
         'type': 'page',
         'target': 'http://localhost:4000/mod/page/view.php?id=19', 'external_id': 19}
    ]

sync_agent_test_data = \
    {
        "statement": {
            "authority": {
                "objectType": "Assistant",
                "name": "New Client",
                "mbox": "mailto:hello@learninglocker.net"
            },
            "stored": "2019-11-26T11:11:56.755Z",
            "context": {
                "platform": "Moodle",
                "language": "en",
                "extensions": {
                    "http://lrs.learninglocker.net/define/extensions/info": {
                        "http://moodle.org": "3.7.2 (Build: 20190909)",
                        "https://github.com/xAPI-vle/moodle-logstore_xapi": "v4.4.0",
                        "event_name": "\\core\\event\\course_module_created",
                        "event_function": "\\src\\transformer\\events\\core\\module_created"
                    }
                },
                "contextActivities": {
                    "grouping": [
                        {
                            "id": "http://localhost:4000",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/lms",
                                "name": {
                                    "en": "\"New Site\""
                                }
                            },
                            "objectType": "Activity"
                        },
                        {
                            "id": "http://localhost:4000/course/view.php?id=2",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/lms/course",
                                "name": {
                                    "en": "Python tutorial"
                                },
                                "extensions": {
                                    "https://w3id.org/learning-analytics/learning-management-system/short-id": "pytut",
                                    "https://w3id.org/learning-analytics/learning-management-system/external-id": ""
                                }
                            },
                            "objectType": "Activity"
                        }
                    ],
                    "category": [
                        {
                            "id": "http://moodle.org",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/source",
                                "name": {
                                    "en": "Moodle"
                                }
                            },
                            "objectType": "Activity"
                        }
                    ]
                }
            },
            "actor": {
                "name": "Admin User",
                "account": {
                    "homePage": "http://localhost:4000",
                    "name": "2"
                },
                "objectType": "Assistant"
            },
            "timestamp": "2019-11-26T11:11:56+00:00",
            "version": "1.0.0",
            "id": "4bc35137-c106-4f6b-86e1-c31c5177978a",
            "verb": {
                "id": "http://activitystrea.ms/schema/1.0/create",
                "display": {
                    "en": "created"
                }
            },
            "object": {
                "id": "http://localhost:4000/mod/book/view.php?id=13",
                "definition": {
                    "type": "http://id.tincanapi.com/activitytype/lms/module",
                    "name": {
                        "en": "Advanced Python"
                    },
                    "extensions": {
                        "https://w3id.org/learning-analytics/learning-management-system/external-id": ""
                    }
                },
                "objectType": "Activity"
            }
        }
    }

sync_agent_test_data_chapter = \
    {
        "statement": {
            "authority": {
                "objectType": "Assistant",
                "name": "New Client",
                "mbox": "mailto:hello@learninglocker.net"
            },
            "stored": "2019-11-26T11:12:27.448Z",
            "context": {
                "platform": "Moodle",
                "language": "en",
                "extensions": {
                    "http://lrs.learninglocker.net/define/extensions/info": {
                        "http://moodle.org": "3.7.2 (Build: 20190909)",
                        "https://github.com/xAPI-vle/moodle-logstore_xapi": "v4.4.0",
                        "event_name": "\\mod_book\\event\\chapter_created",
                        "event_function": "\\src\\transformer\\events\\mod_book\\chapter_created"
                    }
                },
                "contextActivities": {
                    "grouping": [
                        {
                            "id": "http://localhost:4000",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/lms",
                                "name": {
                                    "en": "\"New Site\""
                                }
                            },
                            "objectType": "Activity"
                        },
                        {
                            "id": "http://localhost:4000/course/view.php?id=2",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/lms/course",
                                "name": {
                                    "en": "Python tutorial"
                                },
                                "extensions": {
                                    "https://w3id.org/learning-analytics/learning-management-system/short-id": "pytut",
                                    "https://w3id.org/learning-analytics/learning-management-system/external-id": ""
                                }
                            },
                            "objectType": "Activity"
                        },
                        {
                            "id": "http://localhost:4000/mod/book/view.php?id=13",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/book",
                                "name": {
                                    "en": "Advanced Python"
                                },
                                "extensions": {
                                    "https://w3id.org/learning-analytics/learning-management-system/external-id": ""
                                }
                            },
                            "objectType": "Activity"
                        }
                    ],
                    "category": [
                        {
                            "id": "http://moodle.org",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/source",
                                "name": {
                                    "en": "Moodle"
                                }
                            },
                            "objectType": "Activity"
                        }
                    ]
                }
            },
            "actor": {
                "name": "Admin User",
                "account": {
                    "homePage": "http://localhost:4000",
                    "name": "2"
                },
                "objectType": "Assistant"
            },
            "timestamp": "2019-11-26T11:12:27+00:00",
            "version": "1.0.0",
            "id": "65b7177c-b9a0-4721-b4f9-f77c23c6a041",
            "verb": {
                "id": "http://activitystrea.ms/schema/1.0/create",
                "display": {
                    "en": "created"
                }
            },
            "object": {
                "id": "http://localhost:4000/mod/book/view.php?id=13&chapterid=2",
                "definition": {
                    "type": "http://id.tincanapi.com/activitytype/chapter",
                    "name": {
                        "en": "Advanced lambda statements"
                    },
                    "description": {
                        "en": "yo this is cool man."
                    }
                },
                "objectType": "Activity"
            }
        }
    }

test_parse_quiz_question = \
    {
        "statements": [
            {
                "object": {
                    "id": "http://localhost:4000/mod/quiz/edit.php?cmid=6"
                },
                "context": {
                    "extensions": {
                        "http://activitystrea.ms/schema/1.0/question": [
                            {
                                "question_id": "14",
                                "question_name": "Is SCRUM any good?",
                                "question_text": "<p>Is SCRUM any good?<br></p>"
                            },
                            {
                                "question_id": "15",
                                "question_name": "Is waterfall any good?",
                                "question_text": "<p>Is the waterfall method any good?</p>"
                            }
                        ]
                    }
                }
            }
        ]
    }

test_parse_quiz_question_data = \
    {
        6: [
            {
                'question_id': '14',
                'question_name': 'Is SCRUM any good?',
                'question_text': '<p>Is SCRUM any good?<br></p>'
            },
            {
                'question_id': '15',
                'question_name': 'Is waterfall any good?',
                'question_text': '<p>Is the waterfall method any good?</p>'
            }
        ]
    }

test_no_questions_quiz_question_data = \
    {
        "statements": [
            {
                "verb": {
                    "id": "http://id.tincanapi.com/verb/viewed",
                    "display": {
                        "en": "viewed"
                    }
                },
                "object": {
                    "id": "http://localhost:4000/mod/quiz/edit.php?cmid=27",
                },
                "context": {
                    "extensions": {
                        "http://activitystrea.ms/schema/1.0/question": []
                    }
                }
            }
        ]
    }

test_course_sync_agent_parser = \
    {
        "statement": {
            "authority": {
                "objectType": "Agent",
                "name": "New Client",
                "mbox": "mailto:hello@learninglocker.net"
            },
            "stored": "2019-12-13T09:30:00.522Z",
            "context": {
                "platform": "Moodle",
                "language": "en",
                "extensions": {
                    "http://lrs.learninglocker.net/define/extensions/info": {
                        "http://moodle.org": "3.7.2 (Build: 20190909)",
                        "https://github.com/xAPI-vle/moodle-logstore_xapi": "v4.4.0",
                        "event_name": "\\core\\event\\course_created",
                        "event_function": "\\src\\transformer\\events\\core\\course_created"
                    }
                },
                "contextActivities": {
                    "category": [
                        {
                            "id": "http://moodle.org",
                            "definition": {
                                "type": "http://id.tincanapi.com/activitytype/source",
                                "name": {
                                    "en": "Moodle"
                                }
                            },
                            "objectType": "Activity"
                        }
                    ]
                }
            },
            "actor": {
                "name": "Admin User",
                "account": {
                    "homePage": "http://localhost:4000",
                    "name": "2"
                },
                "objectType": "Agent"
            },
            "timestamp": "2019-12-13T09:30:00+00:00",
            "version": "1.0.0",
            "id": "c8b3de57-d2c3-4acc-bcbd-25d5776b5e63",
            "verb": {
                "id": "http://activitystrea.ms/schema/1.0/create",
                "display": {
                    "en": "created"
                }
            },
            "object": {
                "id": "http://localhost:4000/course/view.php?id=16",
                "definition": {
                    "type": "http://id.tincanapi.com/activitytype/lms/course",
                    "name": {
                        "en": "Ruby tutorial"
                    },
                    "extensions": {
                        "https://w3id.org/learning-analytics/learning-management-system/short-id": "ruby",
                        "https://w3id.org/learning-analytics/learning-management-system/external-id": ""
                    }
                },
                "objectType": "Activity"
            }
        }
    }
