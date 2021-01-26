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
  const response = await fetch(`${remoteUrl}/api/friendships?friend_list=sender_and_receiver`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("accessToken"),
    },
  });
  return await response.json();
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
