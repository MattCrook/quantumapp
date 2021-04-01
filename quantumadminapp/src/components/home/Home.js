import React from "react";
import NavBar from "../nav/Nav";
import "./styles/Home.css";

const Home = (props) => {
  return (
    <>
      <NavBar {...props} />
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
      <div>Info to side</div>
      <div>Currently logged in as</div>
      <div>Last login</div>
      <div>Current time</div>



    </>
  );
};

export default Home;
