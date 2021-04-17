let isLoading = false;
const setIsLoading = (newState) => (isLoading = newState);
const useIsLoading = () => isLoading;

const displayLoadingScreen = () => {
  const mainContainer = document.querySelector(".group_confirm_master_container");
  const loadingDiv = document.getElementById("loading");
  mainContainer.style.display = "none";
  const loadingGraphic = renderLoadingScreen();
  loadingDiv.innerHTML += loadingGraphic;
};

const loading = () => {
  const isLoading = useIsLoading();
  isLoading ? displayLoadingScreen() : null;
};

const backToPreviousPage = () => {
  const URL = window.origin;
  const backToPreviousButton = document.querySelector(".back_to_previous");
  backToPreviousButton.addEventListener("click", async (e) => {
    e.preventDefault();
    window.confirm("Going back will delete this group. Are you sure you want to go back?");
    setIsLoading(true);
    loading();
    const csrftoken = getCookie("csrftoken");

    const response = await fetch(`${URL}/api/group_chats/${e.target.dataset.id}`, {
      method: "DELETE",
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    });
    if (response.ok && response.status === 204) {
      setIsLoading(false);
      loading();
      setTimeout(() => {
        window.location.pathname = "group_chat/";
      }, 1800);
    }
  });
};

const cancelNewGroup = () => {
  const URL = window.origin;
  const cancelButton = document.querySelector(".cancel_group");
  cancelButton.addEventListener("click", async (e) => {
    console.log("groupChatStagingEvents", e);
    e.preventDefault();
      const confirm = window.confirm("Are you sure you want to delete this group?");
      if (confirm) {
          setIsLoading(true);
          loading();
          const csrftoken = getCookie("csrftoken");

          const response = await fetch(`${URL}/api/group_chats/${e.target.dataset.id}`, {
            method: "DELETE",
            mode: "same-origin",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
            },
          });
          if (response.ok && response.status === 204) {
            setIsLoading(false);
            loading();
            setTimeout(() => {
              window.location.pathname = "group_chat/";
            }, 1800);
          }
      } else {
          setIsLoading(false);
          loading();
          window.location.pathname = `group_chat/${e.target.dataset.id}/confirm/`
      }
  });
};

function renderLoadingScreen() {
  return `
        <div class="loading fade_in">
        <div class="loading-text">
            <span class="loading-text-words">L</span>
            <span class="loading-text-words">O</span>
            <span class="loading-text-words">A</span>
            <span class="loading-text-words">D</span>
            <span class="loading-text-words">I</span>
            <span class="loading-text-words">N</span>
            <span class="loading-text-words">G</span>
        </div>
        </div>
    `;
}

function getCookie(name) {
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
}

const init = () => {
  backToPreviousPage();
  cancelNewGroup();
};

init();
