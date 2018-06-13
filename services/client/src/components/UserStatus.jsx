import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

class UserStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      id: '',
      username: '',
      active: '',
      admin: ''
    };
  };
  componentDidMount() {
  	if (this.props.isAuthenticated) {
  	  this.getUserStatus();
  	}
  };
  getUserStatus() {
  	const options = {
  	  url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
  	  methods: 'get',
  	  headers: {
  	  	'Content-Type': 'application/json',
  	  	Authorization: `Bearer ${window.localStorage.authToken}`
  	  }
  	};
  	axios(options)
  	.then((res) => { 
  	  console.log(res.data.data);
      const data = res.data.data;
  	  this.setState({
  	  	email: data.email,
  	  	id: data.id,
  	  	username: data.username,
        active: String(data.active),
        admin: String(data.admin)
  	  })
  	})
  	.catch((error) => { console.log(error) });
  };
  render() {
  	if (!this.props.isAuthenticated) {
  	  return (
        <p>You must be logged in to view this. Click <Link to="/login">here</Link>
          to log back in. </p>
  	  )
  	};    
  	return (
      <div>
        <ul>
          <li><strong>User ID:</strong> {this.state.id}</li>
          <li><strong>Email:</strong> {this.state.email}</li>
          <li><strong>Username:</strong> {this.state.username}</li>
          <li><strong>Active:</strong> {this.state.active}</li>
          <li><strong>Admin:</strong> {this.state.admin}</li>
        </ul>
      </div>
  	)
  };
};

export default UserStatus;