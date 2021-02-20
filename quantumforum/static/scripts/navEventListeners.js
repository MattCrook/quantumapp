import {
  getAllUsersFriends,
  getUserList,
  getUser,
  sendFriendRequest,
  getFriendships,
  getFriendRequests,
  postActivityLogError,
} from "./services.js";


let isLoading = false;
const setIsLoading = (newState) => (isLoading = newState);
const useIsLoading = () => isLoading;


const renderLoading = () => {
  return `
    <main class="modal__content" id="notifications-content">
      <div class="no_notifications_container">
        <div id="loading">
          <div class="loading_text">Loading...</div>
      </div>
    </main>
  `;
}


const showLoading = () => {
  const loadingDiv = document.getElementById("loading_main_container");
  loadingDiv.innerHTML = "";
  const loadingBar = renderLoading();
  loadingDiv.innerHTML += loadingBar;
};

const hideLoading = () => {
  const loadingDiv = document.getElementById("loading_main_container");
  loadingDiv.innerHTML = "";
};


const loading = () => {
  const isLoading = useIsLoading();
  isLoading ? showLoading() : hideLoading();
};

const showModal = () => {
  MicroModal.init({
    openTrigger: "data-micromodal-trigger",
    closeTrigger: "data-micromodal-close",
    openClass: "is-open",
    disableScroll: true,
    disableFocus: false,
    awaitOpenAnimation: true,
    awaitCloseAnimation: false,
    debugMode: true,
  });
};

// Handles the 'X' button in the search users bar.
const closeOverlaySearchBarButton = () => {
  const closeButton = document.querySelector(".overlay_close");
  const searchQuantumResults = document.getElementById("search_quantum_results_master_container");
  const nav = document.querySelector(".nav");
  const currentGroupChats = document.querySelector(".current_group_chats_container");

  const bodyTag = document.getElementsByTagName("body")[0];
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      searchQuantumResults.style.display = "none";
      bodyTag.classList.toggle("overlay");
      closeButton.style.display = "none";
      nav.style.boxShadow = "0px 6px 4px 0px rgb(190 190 190)";
      currentGroupChats.style.boxShadow = "2px 6px 4px 0px rgb(190 190 190)";
    });
  }
};

const handleNavProfileDropdown = () => {
  const profileDropdownContainer = document.getElementById("profile_dropdown_container");
  const navImage = document.querySelector(".nav_image");
  const close = () => (profileDropdownContainer.style.display = "none");
  const open = () => (profileDropdownContainer.style.display = "block");

  navImage.addEventListener("click", () => {
    const display = profileDropdownContainer.style.display;
    display === "none" && open();
    display === "block" && close();
  });
};

const handleClearSessionStorage = () => {
  const backBtn = document.querySelector(".back_btn");
  const goToProfileBtn = document.getElementById("go_to_profile");
  const goHomeButton = document.getElementById("go_home");

  backBtn.addEventListener("click", () => {
    sessionStorage.clear();
  });
  goToProfileBtn.addEventListener("click", () => {
    sessionStorage.clear();
  });
  goHomeButton.addEventListener("click", () => {
    sessionStorage.clear();
  });
};

const handleShowNotifications = () => {
  const notificationsButton = document.querySelector(".notifications_header");
  const friendsListModalContainer = document.querySelector(".friends_list");
  const friendsButton = document.querySelector(".friends_header");

  notificationsButton.addEventListener("click", () => {
    friendsListModalContainer.style.display = "none";
    notificationsButton.style.display = "none";
    friendsButton.style.display = "block";
    setIsLoading(true);
    loading();

    Promise.all([getUser(), getFriendships(), getFriendRequests()]).then(response => {
      const currentUser = response[0];
      const allSenderAndReceiver = response[1];
      const allFriendRequests = response[2];
      const friendRequestsUserHasSent = allSenderAndReceiver.filter((request) => request.requester.id === currentUser.id);
      const friendRequestsUserHasReceived = allSenderAndReceiver.filter(
        (request) => request.addressee.id === currentUser.id
      );
      const allSentAndReceivedFriendships = [...friendRequestsUserHasSent, ...friendRequestsUserHasReceived];
      const senderAndReceiverIds = allSentAndReceivedFriendships.map((friendship) => friendship.id);
      const allUsersFriendRequests = allFriendRequests.filter(
        (friendRequest) => !senderAndReceiverIds.includes(friendRequest.sender_and_receiver_id)
      );
      setIsLoading(false);
      loading();

      allUsersFriendRequests.forEach(friendRequest => {
        const hasNotifications = friendRequest.sender_and_receiver.addressee && friendRequest.sender_and_receiver.addressee.id === currentUser.id ? true : false;
        const notification = "Friend Request";
          showNotificationsBody(friendRequest.sender_and_receiver.requester, hasNotifications, notification);
      })
    })
  });
};

const showNotificationsBody = (friend, hasNotifications, notification) => {
  const notificationsContainer = document.querySelector(".notifications");
  notificationsContainer.style.display = "block";
  notificationsContainer.innerHTML = "";
  const renderNotificationCards = renderNotifications(friend, hasNotifications, notification);
  notificationsContainer.innerHTML += renderNotificationCards;
};

const handleShowFriendsList = () => {
  const notificationsButton = document.querySelector(".notifications_header");
  const friendsListModalContainer = document.querySelector(".friends_list");
  const friendsButton = document.querySelector(".friends_header");
  const notificationsContainer = document.querySelector(".notifications");

  friendsButton.addEventListener("click", () => {
    notificationsButton.style.display = "block";
    friendsListModalContainer.style.display = "block";
    friendsButton.style.display = "none";
    notificationsContainer.style.display = "none";
  });
};

function renderNotifications(friend, hasNotifications, notification) {
  const defaultProfilePicture = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  let profilePicture;
  friend && friend.image && friend.image.image ? profilePicture = friend.image.image : profilePicture = defaultProfilePicture;

  if (hasNotifications) {
    return `
        <main class="modal__content" id="notifications-content">
        <div class="friends_list_container">
            <div class="friend_card">
                <div id="friend_card_container_1">
                    <div class="friend_profile_pic">
                        <img class="friend_card_img" src="${profilePicture}" />
                    </div>
                    <div class="friend_name">${friend.first_name} ${friend.last_name}</div>
                    <div class="notification_type">${notification}</div>
                </div>
                <div id="friend_card_container_2">
                    <div class="accept_button">Accept</div>
                    <div class="decline_button">Decline</div>
                    <div class="block_button">Block User</div>
                </div>
            </div>
        </div>

        <footer class="modal__footer">
            <button class="modal__btn" data-micromodal-close
                aria-label="Close this dialog window">Close</button>
        </footer>
      </main>
    `;
  } else if (!hasNotifications) {
    return `
    <main class="modal__content" id="notifications-content">
      <div class="no_notifications_container">
          <div class="no_notifications">None</div>
      </div>
      <footer class="modal__footer">
          <button class="modal__btn" data-micromodal-close
              aria-label="Close this dialog window">Close</button>
      </footer>
    </main>
    `;
  } else {
    return `
    <main class="modal__content" id="notifications-content">
    <div class="error_container>
        <div class="no_notifications">Oops! Something went wrong loading your notifications.</div>
    </div>
    <footer class="modal__footer">
        <button class="modal__btn" data-micromodal-close
            aria-label="Close this dialog window">Close</button>
    </footer>
  </main>
    `;
  }
}

const initNav = () => {
  showModal();
  closeOverlaySearchBarButton();
  handleNavProfileDropdown();
  handleClearSessionStorage();
  handleShowNotifications();
  handleShowFriendsList();
};

initNav();
