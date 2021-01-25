const remoteUrl = process.env.REMOTE_API_URL;

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
