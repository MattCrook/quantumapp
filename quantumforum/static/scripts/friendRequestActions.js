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
        const friendRequestId = e.target.dataset.friendRequest;

        const data = {
            id: friendRequestId,
            statusCode: 2,
            lastUpdatedBy: authUser.id
        }

        updateFriendRequest(data).then(friendRequest => {

        })

    });
  });
};

const initActions = () => {
  getUser().then((response) => {
    setCurrentAuthUser([response]);
    getUserList().then((users) => {
      setAllUsers(users);
      handleAcceptFriendRequest();
    });
  });
};

initActions();
