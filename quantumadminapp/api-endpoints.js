import env from "./env-config.json";

const api_endpoints_config = {
    "parks": `${env.API_URL}/api/parks`,
    "tracktypes": `${env.API_URL}/api/tracktypes`,
    "manufacturers": `${env.API_URL}/api/manufacturers`,
    "rollercoasters": `${env.API_URL}/api/rollercoasters`,
    "userprofiles": `${env.API_URL}/api/userprofiles`,
    "credits": `${env.API_URL}/api/credits`,
    "messages": `${env.API_URL}/api/messages`,
    "users": `${env.API_URL}/api/users`,
    "images": `${env.API_URL}/api/images`,
    "credentials": `${env.API_URL}/api/credentials`,
    "news": `${env.API_URL}/api/news`,
    "contributor_applications": `${env.API_URL}/api/contributor_applications`,
    "activity_log": `${env.API_URL}/api/activity_log`,
    "login_info": `${env.API_URL}/api/login_info`,
    "calendar_events": `${env.API_URL}/api/calendar_events`,
    "error_logs": `${env.API_URL}/api/error_logs`,
    "user_feedback": `${env.API_URL}/api/user_feedback`,
    "bug_reports": `${env.API_URL}/api/bug_reports`,
    "status_code": `${env.API_URL}/api/status_code`,
    "friend_requests": `${env.API_URL}/api/friend_requests`,
    "friendships": `${env.API_URL}/api/friendships`,
    "app_login_data": `${env.API_URL}/api/app_login_data`,
    "group_chats": `${env.API_URL}/api/group_chats`,
    "friends": `${env.API_URL}/api/friends`,
    "friends_join": `${env.API_URL}/api/friends_join`,
}

export { api_endpoints_config };
