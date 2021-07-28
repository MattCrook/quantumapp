import React, {useEffect, useState}from "react";
import { useAuthUser } from "../../contexts/AuthUserContext";
import {getRequestData} from "../../modules/services.js"
import NavBar from "../nav/Nav";
import "./styles/Home.css";

const Home = (props) => {
  //const [authMethod, setAuthMethod] = useState('');
  const [backend, setBackend] = useState('');
  const { authUser, authUserData } = useAuthUser();

  let currentDate = new Date().toLocaleString("en-US");
  const lastLoginDatetime = props.authUser.last_login.split("+")[0]
  const lastLogin = new Date(lastLoginDatetime).toLocaleString("en-US");
  console.log(authUserData)

  function getBackend(backendFullname) {
    const backend = backendFullname.split(".")[1] === "auth0_backend" ? backendFullname.split(".")[2] : backendFullname.split(".")[3]
    setBackend(backend);
  }

  useEffect(() => {
    // const requestData = async () => {
    //   const response = await getRequestData();
    //   console.log(response)
    // }
    // requestData();
    getBackend(authUser.session_data._auth_user_backend)

  }, []);



  return (
    <>
      <NavBar {...props} />
      <div id="home_main_container">
        <div id="home_main_column_1">
          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Accounts</div>
            </div>
            <div className="home_section_item">Email Addresses</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Auth Tokens</div>
            </div>
            <div className="home_section_item">Tokens</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Authorization</div>
            </div>
            <div className="home_section_item">Groups</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Social Auth</div>
            </div>
            <div className="home_section_item">Associations</div>
            <div className="home_section_item">Nonces</div>
            <div className="home_section_item">User Social Auths</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">QuantumAPI</div>
            </div>
            <div className="home_section_item">Auth User</div>
            <div className="home_section_item">User Profile</div>
            <div className="home_section_item">Credentials</div>
            <div className="home_section_item">App Login Data</div>
            <div className="home_section_item">Activity Logs</div>
            <div className="home_section_item">User Login History</div>
            <div className="home_section_item">Error Logs</div>
            <div className="home_section_item">Bug Report Submissions</div>
            <div className="home_section_item">Feedback Submissions</div>
            <div className="home_section_item">Blog Applications</div>
            <div className="home_section_item">Calendar Events</div>
            <div className="home_section_item">Roller Coasters</div>
            <div className="home_section_item">Parks</div>
            <div className="home_section_item">Manufacturers</div>
            <div className="home_section_item">Tracktypes</div>
            <div className="home_section_item">Credits</div>
            <div className="home_section_item">News Articles</div>
            <div className="home_section_item">Messages</div>
            <div className="home_section_item">Images</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Quantum Forum</div>
            </div>
            <div className="home_section_item">User's Friends</div>
            <div className="home_section_item">Friend Requests</div>
            <div className="home_section_item">FriendJoin</div>
            <div className="home_section_item">FriendShips</div>
            <div className="home_section_item">Group Chats</div>
            <div className="home_section_item">Private Chats</div>
            <div className="home_section_item">Group Members Join</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Sessions</div>
            </div>
            <div className="home_section_item">Sessions</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Sites</div>
            </div>
            <div className="home_section_item">Sites</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Social Accounts</div>
            </div>
            <div className="home_section_item">Social Accounts</div>
            <div className="home_section_item">Social Applications</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Social Authentication</div>
            </div>
            <div className="home_section_item">Social Codes</div>
            <div className="home_section_item">Social Tokens</div>
          </div>

          <div className="home_section_container">
            <div className="home_title_wrapper">
              <div className="home_section_title">Migrations</div>
            </div>
            <div className="home_section_item">Migrations</div>
          </div>
        </div>

        <div id="home_main_column_2">
          <div className="side_login_info_title">Your Info:</div>
          <div className="side_info_wrapper">
            <div className="side_info_row_title">Currently Logged In As:</div>
            <div className="side_info_item">{props.authUser.email}</div>
          </div>

          <div className="side_info_wrapper">
            <div className="side_info_row_title">Username:</div>
          <div className="side_info_item">{props.authUser.username}</div>
          </div>

          <div className="side_info_wrapper">
            <div className="side_info_row_title">Authenticated Through:</div>
            {/* Get authentication app / Associations / backends? / where user logged in thru */}
              <div className="side_info_item">QuantumAdminApp</div>
          </div>
          <div className="side_info_wrapper">
            <div className="side_info_row_title">Auth Method:</div>
            <div className="side_info_item">{backend}</div>
          </div>

          <div className="side_info_wrapper">
            <div className="side_info_row_title">Groups/Role(s):</div>
            <div className="side_info_ul">
              <li className="side_info_item">Group: (if any)</li>
              <li className="side_info_item">Role: (title/ permissions?/ IAM policy name etc..</li>
            </div>
          </div>

          <div className="side_info_wrapper">
            <div className="side_info_row_title">Last login:</div>
          <div className="side_info_item">{lastLogin}</div>
          </div>

          <div className="side_info_wrapper">
            <div className="side_info_row_title">Current time:</div>
            <div className="side_info_item">{currentDate}</div>
            </div>
        </div>
      </div>
    </>
  );
};

export default Home;
