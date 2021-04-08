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
      console.log(response)
    return await response.json();
  } catch (err) {
    console.log(err);
  }
}
