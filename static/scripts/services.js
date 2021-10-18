const remoteUrl = window.origin;


const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

export async function getUser() {
  try {
    let cookie = getCookie("csrftoken");
    const response = await fetch(`${remoteUrl}/get_auth_user/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cookie,
        Authorization: "Token " + sessionStorage.getItem("token"),
      },
      Accept: "application/json",
    });
    return await response.json();
  } catch (err) {
    console.log(err);
  }
}

export async function getUserList() {
  const token = sessionStorage.getItem("token");
  const response = await fetch(`${remoteUrl}/api/userprofiles`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Token " + token,
    },
  });
  return await response.json();
}

export async function retrieveUserProfile(uid) {
  const token = sessionStorage.getItem("token");
  const response = await fetch(`${remoteUrl}/api/userprofiles/${uid}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Token " + token,
    },
  });
  return await response.json();
}

export async function sendFriendRequest(payload) {
  try {
    let cookie = getCookie("csrftoken");
    const response = await fetch(`${remoteUrl}/api/friend_requests`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cookie,
        Authorization: "Token " + sessionStorage.getItem("token"),
      },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function updateStatusCode(code) {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/status_code`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
      body: JSON.stringify(code),
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function getAllUsersFriends() {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/friendships?friend_list=sender_and_receiver`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function getFriendships() {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/friendships`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function getFriendRequests() {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/friend_requests`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function updateFriendRequest(data) {
  try {
    let cookie = getCookie("csrftoken");
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/friend_requests/${data.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cookie,
        Authorization: "Token " + token,
      },
      body: JSON.stringify(data),
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function getAllUsersFriendsFromReceiver(userId) {
  const token = sessionStorage.getItem("token");
  const response = await fetch(`${remoteUrl}/api/friendships?addressee=${userId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Token " + token,
    },
  });
  return await response.json();
}

export async function sendAppLoginData(payload) {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/api/app_login_data`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}

export async function retrieveUserSessionData() {
  try {
    const token = sessionStorage.getItem("token");
    const response = await fetch(`${remoteUrl}/get_user_session`, {
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

export async function getGroupChat(groupId) {
  try {
    const token = sessionStorage.getItem("token");
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

export async function postActivityLogError(error, appName, fileName, functionName, userId) {
  try {
    const token = sessionStorage.getItem("token");
    const payload = {
      message: error.message,
      stack: error.stack,
      component: fileName,
      error: error,
      appName: appName,
      callingFunction: functionName,
      time: date,
      sessionId: getCookie("sessionid"),
      userId: userId,
    }
    const response = await fetch(`${remoteUrl}/api/error_logs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.log(error);
  }
}
