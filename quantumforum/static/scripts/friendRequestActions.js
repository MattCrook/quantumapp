import { useAuthUser, useUserList } from "./hooks.js";
import { getUser, getUserList, updateFriendRequest } from "./services.js";

const declineButton = document.querySelector(".decline_button");
const blockButton = document.querySelector(".block_button");
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
      });
    });
  });
};

function displayAccepted(friendId, friendRequestId) {
    return `
    <div id="friend_card_container_2" data-friendrequest="${friendRequestId}">
        <div class="accepted_banner" data-id="${friendId}">Accepted</div>
    </div>
    `
}

const initActions = () => {
  getUser().then((response) => {
    setCurrentAuthUser([response]);
    getUserList().then((users) => {
      setAllUsers(users);
      handleAcceptFriendRequest();
    });
  });
};

export { initActions };
