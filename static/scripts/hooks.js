const useQuantumFriends = () => {
    let friends = [];
      return [
          () => friends.slice(),
          (newFriends) => (friends = newFriends.splice(0))
      ];
  };

const useUserList = () => {
    let users = [];
        return [
            () => users.slice(),
            (newUsers) => (users = newUsers.splice(0))
    ];
};

const useLoading = (initialState) => {
    let isLoading = initialState;
        return [
            () => isLoading,
            (newState) => (isLoading = newState)
        ];
    };

// need to be able to add a new entry to Array
// pass in updated state and that be the array without the old state.
const useGroupChatParticipants = () => {
    let participantsInState = [];
        return [
            () => participantsInState.slice(),
            (newParticipantList) => (participantsInState = newParticipantList.splice(0))
        ];
    };
const useGroup = (participants) => {
    let group = participants;
        return [
            () => group.slice(),
            (newGroup) => (group = newGroup.splice(0))
        ];
};

const useAddedToGroup = () => {
    let userProfile = [];
        return [
            () => userProfile.slice(),
            (newUser) => (userProfile = newUser.splice(0))
        ];
}

const useAuthUser = () => {
    let authUser = [];
        return [
            () => authUser.slice(),
            (newAuthUser) => (authUser = newAuthUser.splice(0))
        ];
}

export { useQuantumFriends, useUserList, useLoading, useGroupChatParticipants, useGroup, useAddedToGroup, useAuthUser };
