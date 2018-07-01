import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';

import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import Exercises from './components/Exercises';

class App extends Component {
  constructor() {
    super();
    this.state = {
    	users: [],
    	username: '',
    	email: '',
      admin: false,
      title: 'Crypto App',
      isAuthenticated: false,
    };
    this.handleChange = this.handleChange.bind(this);
    this.loginUser = this.loginUser.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  };
  componentWillMount() {
    if (window.localStorage.getItem('authToken')) {
      this.setState({ isAuthenticated: true});
    };
  };
  componentDidMount() {
  	this.getUsers();
  };
  getUsers() {
  	axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
  	.then((res) => { this.setState({ users: res.data.data.users }); })
  	.catch((err) => { console.log(err); });
  };
  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  };
  loginUser(token) {
    window.localStorage.setItem('authToken', token);
    this.setState({ isAuthenticated: true });
    this.getUsers();
  };
  handleChange(event) {
  	const obj = {};
  	obj[event.target.name] = event.target.value;
  	this.setState(obj);
  };

  render() {
  	return (
      <div>
        <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated} />
  	    <div className="container">
          <div className="row">
            <div className="col-md-6">
              <br/>
              <Switch>
                <Route exact path='/' render={() => (
                  <Exercises isAuthenticated={this.state.isAuthenticated}/>                  
                )} />
                <Route exact path='/about' component={About} />
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    isAuthenticated={this.state.isAuthenticated}
                    loginUser={this.loginUser}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'Login'}
                    formData={this.state.formData}
                    isAuthenticated={this.state.isAuthenticated}
                    loginUser={this.loginUser}
                  />
                )} />
                <Route exact path='/logout' render={() => (
                  <Logout
                    logoutUser={this.logoutUser}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
                <Route exact path='/status' render={() => (
                  <UserStatus
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    )
  };
}

export default App;