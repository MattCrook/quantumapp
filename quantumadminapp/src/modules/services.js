import env from "../../env-config.json";
const remoteURL = env.API_URL;

export async function healthCheck() {
  try {
    const token = sessionStorage.getItem("QuantumToken");
    const response = await fetch(`${remoteURL}/api/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    return response;
  } catch (err) {
    console.log(err);
  }
}

export async function getRequestData() {
  try {
    const token = sessionStorage.getItem("QuantumToken");
    const response = await fetch(`${remoteURL}/api/request_data`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    return response;
  } catch (err) {
    console.log(err);
  }
}
