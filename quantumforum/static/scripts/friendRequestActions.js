import { useAuthUser, useUserList } from "./hooks.js";
import { getUser, getUserList, updateFriendRequest } from "./services.js";


const [currentAuthUser, setCurrentAuthUser] = useAuthUser();
const [allUsers, setAllUsers] = useUserList();

const handleAcceptFriendRequest = () => {
  const authUser = currentAuthUser();
  const users = allUsers();
  const acceptButtonNodes = document.querySelectorAll(".accept_button");
  const acceptButtons = Array.from(acceptButtonNodes);
  acceptButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const dataFriendId = e.target.dataset.id;
      const friendRequestId = e.target.dataset.friendrequest;

      const data = {
        id: friendRequestId,
        statusCode: 2,
        lastUpdatedBy: authUser[0].id,
      };

      updateFriendRequest(data).then((friendRequest) => {
        console.log({ friendRequest });
          console.log(e.target);
        const friendCardContainer2 = e.target.parentNode;
        friendCardContainer2.innerHTML = "";
        const renderAccepted = displayAccepted(dataFriendId, friendRequestId);
          friendCardContainer2.innerHTML += renderAccepted;
          const friendsButton = document.querySelector(".friends_header");

          friendsButton.addEventListener("click", () => {
              const friendsList = document.getElementById("friends");
              friendsList.innerHTML = "";
            //   const usersFriends = 

          })
      });
    });
  });
};
const handleDeclinedFriendRequest = () => {
  const authUser = currentAuthUser();
  const users = allUsers();
  const declineButtonNodes = document.querySelectorAll(".decline_button");
  const declineButtons = Array.from(declineButtonNodes);
  declineButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const dataFriendId = e.target.dataset.id;
      const friendRequestId = e.target.dataset.friendrequest;

      const data = {
        id: friendRequestId,
        statusCode: 4,
        lastUpdatedBy: authUser[0].id,
      };

      updateFriendRequest(data).then((friendRequest) => {
        console.log({ friendRequest });
        console.log(e.target);

        const friendCardContainer2 = e.target.parentNode;
        friendCardContainer2.innerHTML = "";
        const renderDeclined = displayDeclined(dataFriendId, friendRequestId);
        friendCardContainer2.innerHTML += renderDeclined;
      });
    });
  });
};

const handleBlockedFriendRequest = () => {
  const authUser = currentAuthUser();
  const users = allUsers();
  const blockButtonNodes = document.querySelectorAll(".block_button");
  const blockButtons = Array.from(blockButtonNodes);
  blockButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const dataFriendId = e.target.dataset.id;
      const friendRequestId = e.target.dataset.friendrequest;

      const data = {
        id: friendRequestId,
        statusCode: 3,
        lastUpdatedBy: authUser[0].id,
      };

      updateFriendRequest(data).then((friendRequest) => {
        console.log({ friendRequest });
        console.log(e.target);

        const friendCardContainer2 = e.target.parentNode;
        friendCardContainer2.innerHTML = "";
        const renderBlocked = displayBlocked(dataFriendId, friendRequestId);
        friendCardContainer2.innerHTML += renderBlocked;
      });
    });
  });
};

function displayAccepted(friendId, friendRequestId) {
  return `
    <div id="friend_card_container_2" data-friendrequest="${friendRequestId}">
        <div class="accepted_banner" data-id="${friendId}">Accepted</div>
    </div>
    `;
}

function displayDeclined(friendId, friendRequestId) {
  return `
    <div id="friend_card_container_2" data-friendrequest="${friendRequestId}">
        <div class="accepted_banner" data-id="${friendId}">Declined</div>
    </div>
    `;
}

function displayBlocked(friendId, friendRequestId) {
  return `
    <div id="friend_card_container_2" data-friendrequest="${friendRequestId}">
        <div class="accepted_banner" data-id="${friendId}">Blocked</div>
    </div>
    `;
}

const initActions = () => {
  getUser().then((response) => {
    setCurrentAuthUser([response]);
    getUserList().then((users) => {
      setAllUsers(users);
      handleAcceptFriendRequest();
      handleDeclinedFriendRequest();
      handleBlockedFriendRequest();
    });
  });
};

export { initActions };
