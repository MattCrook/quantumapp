// import env from "./env-config.json";
const URL = window._env_.API_URL

const api_endpoints_config = {
    "parks": `${URL}/api/parks`,
    "tracktypes": `${URL}/api/tracktypes`,
    "manufacturers": `${URL}/api/manufacturers`,
    "rollercoasters": `${URL}/api/rollercoasters`,
    "userprofiles": `${URL}/api/userprofiles`,
    "credits": `${URL}/api/credits`,
    "messages": `${URL}/api/messages`,
    "users": `${URL}/api/users`,
    "images": `${URL}/api/images`,
    "credentials": `${URL}/api/credentials`,
    "news": `${URL}/api/news`,
    "contributor_applications": `${URL}/api/contributor_applications`,
    "activity_log": `${URL}/api/activity_log`,
    "login_info": `${URL}/api/login_info`,
    "calendar_events": `${URL}/api/calendar_events`,
    "error_logs": `${URL}/api/error_logs`,
    "user_feedback": `${URL}/api/user_feedback`,
    "bug_reports": `${URL}/api/bug_reports`,
    "status_code": `${URL}/api/status_code`,
    "friend_requests": `${URL}/api/friend_requests`,
    "friendships": `${URL}/api/friendships`,
    "app_login_data": `${URL}/api/app_login_data`,
    "group_chats": `${URL}/api/group_chats`,
    "friends": `${URL}/api/friends`,
    "friends_join": `${URL}/api/friends_join`,
}

export { api_endpoints_config };
