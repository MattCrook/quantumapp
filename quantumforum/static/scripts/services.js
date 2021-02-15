// const remoteUrl = process.env.REMOTE_API_URL;
const remoteUrl = "http://localhost:8000";

export async function getUserList() {
  const response = await fetch(`${remoteUrl}/api/userprofiles`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
  });
  return await response.json();
}

export async function retrieveUserProfile(uid) {
  const response = await fetch(`${remoteUrl}/api/userprofiles/${uid}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
  });
  return await response.json();
}

export async function sendFriendRequest(payload) {
  const response = await fetch(`${remoteUrl}/api/friend_request`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
    body: JSON.stringify(payload),
  });
  return await response.json();
}

export async function updateStatusCode(code) {
  const response = await fetch(`${remoteUrl}/api/status_code`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
    body: JSON.stringify(code),
  });
  return await response.json();
}

export async function getAllUsersFriends() {
  try {
    const response = await fetch(`${remoteUrl}/api/friendships?friend_list=sender_and_receiver`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
      },
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function getAllUsersFriendsFromReceiver(userId) {
  const response = await fetch(`${remoteUrl}/api/friendships?addressee=${userId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
  });
  return await response.json();
}

export async function sendAppLoginData(payload) {
  const response = await fetch(`${remoteUrl}/api/app_login_data`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
    body: JSON.stringify(payload),
  });
  return await response.json();
}

export async function retrieveUserSessionData() {
  try {
    const response = await fetch(`${remoteUrl}/get_user_session`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      Accept: "application/json",
    });
    return await response.json();
  } catch (err) {
    console.log(err);
  }
}

export async function getGroupChat(groupId) {
  const token = sessionStorage.getItem("token");
  try {
    const response = await fetch(`${remoteUrl}/api/group_chats/${groupId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
      Accept: "application/json",
    });
    return await response.json();
  } catch (err) {
    console.log(err);
  }
}
