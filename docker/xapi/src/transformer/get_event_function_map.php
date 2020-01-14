<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

namespace src\transformer;
defined('MOODLE_INTERNAL') || die();

function get_event_function_map() {
    $availableevents = [
    // Unnecessary events are omitted from the list, if you need these functions, just remove the //
    // If you plan on using an omitted event, make sure to update the corresponding test.php in tests
        '\core\event\course_completed' => 'core\course_completed', // Feedback assistant
        '\core\event\course_viewed' => 'core\course_viewed', // Inactivity check
        '\core\event\course_created' => 'core\course_created',
        '\core\event\course_updated' => 'core\course_updated', // Update Mofa database
        '\core\event\course_deleted' => 'core\course_deleted', // Update Mofa database
        '\core\event\user_created' => 'core\user_created',
        '\core\event\user_deleted' => 'core\user_deleted', // Update Mofa database
        '\core\event\user_enrolment_created' => 'core\user_enrolment_created',
        '\core\event\role_assigned' => 'core\user_role_assigned', // Update Mofa database
        '\core\event\role_unassigned' => 'core\user_role_unassigned', // Update Mofa database
        '\core\event\user_loggedin' => 'core\user_loggedin',
        '\core\event\user_loggedout' => 'core\user_loggedout',
        '\core\event\course_module_completion_updated' => 'core\course_module_completion_updated', // Feedback assistant
        '\core\event\message_sent' => 'core\message_sent',
        '\core\event\course_module_created' => 'core\module_created', // Update Mofa database
        '\core\event\course_module_updated' => 'core\module_updated', // Update Mofa database
        '\core\event\course_module_deleted' => 'core\module_deleted', // Update Mofa database
        '\mod_assign\event\assessable_submitted' => 'mod_assign\assignment_submitted', // Feedback assistant
        '\mod_assign\event\submission_graded' => 'mod_assign\assignment_graded',
        // '\mod_book\event\course_module_viewed' => 'mod_book\course_module_viewed',
        // '\mod_book\event\chapter_viewed' => 'mod_book\chapter_viewed',
        '\mod_book\event\chapter_created' =>'mod_book\chapter_created', // Update Mofa database
        '\mod_book\event\chapter_updated' => 'mod_book\chapter_updated', // Update Mofa database
        '\mod_book\event\chapter_deleted' => 'mod_book\chapter_deleted', // Update Mofa database
        // '\mod_chat\event\course_module_viewed' => 'mod_chat\course_module_viewed',
        // '\mod_choice\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_data\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_facetoface\event\cancel_booking' => 'mod_facetoface\cancel_booking',
        // '\mod_facetoface\event\course_module_viewed' => 'mod_facetoface\course_module_viewed',
        // '\mod_facetoface\event\signup_success' => 'mod_facetoface\signup_success',
        // '\mod_facetoface\event\take_attendance' => 'mod_facetoface\take_attendance',
        // '\mod_feedback\event\course_module_viewed' => 'mod_feedback\course_module_viewed',
        // '\mod_feedback\event\response_submitted' => 'mod_feedback\response_submitted\handler',
        // '\mod_folder\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_forum\event\course_module_viewed' => 'mod_forum\course_module_viewed',
        // '\mod_forum\event\discussion_viewed' => 'mod_forum\discussion_viewed',
        '\mod_forum\event\discussion_created' => 'mod_forum\discussion_created',
        // '\mod_forum\event\user_report_viewed' => 'mod_forum\user_report_viewed',
        '\mod_forum\event\post_created' => 'mod_forum\post_created',
        // '\mod_glossary\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_imscp\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_lesson\event\course_module_viewed' => 'mod_lesson\course_module_viewed',
        // '\mod_lti\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_page\event\course_module_viewed' => 'mod_page\course_module_viewed',
        // '\mod_quiz\event\course_module_viewed' => 'mod_quiz\course_module_viewed',
        '\mod_quiz\event\attempt_abandoned' => 'mod_quiz\attempt_submitted\handler',
        '\mod_quiz\event\attempt_started' => 'mod_quiz\attempt_started',
        '\mod_quiz\event\edit_page_viewed' => 'mod_quiz\edit_page_viewed', // Retrieve quiz questions
        '\mod_quiz\event\attempt_reviewed' => 'mod_quiz\attempt_reviewed',
        '\mod_quiz\event\attempt_submitted' => 'mod_quiz\attempt_submitted\handler',
        // '\mod_quiz\event\attempt_viewed' => 'mod_quiz\attempt_viewed',
        // '\mod_resource\event\course_module_viewed' => 'mod_resource\course_module_viewed',
        // '\mod_scorm\event\course_module_viewed' => 'mod_scorm\course_module_viewed',
        // '\mod_scorm\event\sco_launched' => 'mod_scorm\sco_launched',
        // '\mod_scorm\event\scoreraw_submitted' => 'mod_scorm\scoreraw_submitted',
        // '\mod_scorm\event\status_submitted' => 'mod_scorm\status_submitted',
        // '\mod_survey\event\course_module_viewed' => 'mod_survey\course_module_viewed',
        // '\mod_url\event\course_module_viewed' => 'mod_url\course_module_viewed',
        // '\mod_wiki\event\course_module_viewed' => 'all\course_module_viewed',
        // '\mod_workshop\event\course_module_viewed' => 'all\course_module_viewed',
        '\totara_program\event\program_assigned' => 'totara_program\program_assigned'
    ];

    $environmentevents = class_exists("report_eventlist_list_generator") ? array_keys(\report_eventlist_list_generator::get_all_events_list(false)) : array_keys($availableevents);

    return array_filter($availableevents, function($k) use ($environmentevents) {
        return in_array($k, $environmentevents);
    }, ARRAY_FILTER_USE_KEY);
}