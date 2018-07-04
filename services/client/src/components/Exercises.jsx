import React, { Component } from 'react';
import { Button, Glyphicon } from 'react-bootstrap';
import AceEditor from 'react-ace';
import axios from 'axios';
import 'brace/mode/python';
import 'brace/theme/solarized_dark';


class Exercises extends Component {
  constructor (props) {
  	super(props)
  	this.state = {
  	  exercises: [],
  	  editor: {
  	  	value: '# Enter your code here.',
        button: {
          isDisabled: false
        },
        isGrading: false,
        isCorrect: false,
        isIncorrect: false
  	  },
  	};
  	this.onChange = this.onChange.bind(this);
  	this.submitExercise = this.submitExercise.bind(this);
  };
  componentDidMount() {
  	this.getExercises();
  };
  onChange(value) {
    const newEditorState = Object.assign({}, this.state.editor, {value: value})
  	this.setState(Object.assign({}, this.state, {editor: newEditorState}));
  };
  submitExercise(event) {
  	event.preventDefault();
    const newEditorState = Object.assign(
      {}, 
      this.state.editor,
      {
        isGrading: true,
        isCorrect: false,
        isIncorrect: false,
        button: {
          isDisabled: true
        }
      }
    )
    this.setState(Object.assign({}, this.state, {editor: newEditorState}))
    const data = { answer: this.state.editor.value };
    const url = process.env.REACT_APP_API_GATEWAY_URL;
    axios.post(url, data)
    .then((res) => {
      const newEditorState = Object.assign({}, this.state.editor)
      newEditorState.isGrading = false
      newEditorState.button.isDisabled = false
      if (res.data == true) {newEditorState.isCorrect = true}
      if (res.data == false) {newEditorState.isIncorrect = true}
      this.setState(Object.assign({}, this.state, {editor: newEditorState}))
      console.log(res) 
    })
    .catch((err) => {
      const newEditorState = Object.assign(
        {},
        this.state.editor,
        {
          isGrading: false,
          button: {
            isDisabled: false
          }
        }
      )
      this.setState(Object.assign({}, this.state, {editor: newEditorState})) 
      console.log(err)
    })
  };
  getExercises() {
    axios.get(`${process.env.REACT_APP_EXERCISES_SERVICE_URL}/exercises`)
    .then((res) => { this.setState({ exercises: res.data.data.exercises }) })
    .catch((err) => { console.log(err) }) 
    //const exercises = [
      //{
  	    //id:	0,
  	    //body:	`Define	a	function	called	sum	that	takes
  	    //two	integers	as	arguments	and	returns	their	sum.`
      //},
      //{
  	    //id:	1,
  	    //body:	`Define	a	function	called	reverse	that	takes	a	string
  	    //as	an	argument	and	returns	the	string	in	reversed	order.`
      //},
      //{
  	    //id:	2,
  	    //body:	`Define	a	function	called	factorial	that	takes	a	random
  	    //number	as	an	argument	and	then	returns	the	factorial	of	that
  	    //given	number.`,
      //}
    //];
    //this.setState({ exercises: exercises });
  };
  render() {
  	return (
  	  <div>
  	    <h1>Exercises</h1>
  	    <hr/><br/>
  	    {!this.props.isAuthenticated &&
  	      <div>
  	        <div className="alert alert-warning">
  	          <span
  	            className="glyphicon glyphicon-exclamation-sign"
  	            aria-hidden="true">
  	          </span>
  	          <span>&nbsp;Please log in to submit an exercise.</span>
  	        </div>
  	        <br/>
  	      </div>
  	    }
  	    {this.state.exercises.length &&
  	      <div key={this.state.exercises[0].id}>
  	        <h4>{this.state.exercises[0].body}</h4>
  	        <AceEditor
              mode="python"
              theme="solarized_dark"
              name={(this.state.exercises[0].id).toString()}
              fontSize={14}
              height={'175px'}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              value={this.state.editor.value}
              style={{
                marginBottom: '10px'
              }}
              onChange={this.onChange}
            />
            {this.props.isAuthenticated &&
              <Button 
                bsStyle="primary" 
                bsSize="small" 
                onClick={this.submitExercise}
                disabled={this.state.editor.button.isDisabled}
              >Run Code</Button>
            }
            {this.state.editor.isGrading && 
              <h4>
                &nbsp;
                <Glyphicon glyph="repeat" className="glyphicon-spin"/>
                &nbsp;
                Grading...
              </h4>
            }
            {this.state.editor.isCorrect &&
              <h4>
                &nbsp;
                <Glyphicon glyph="ok" className="glyphicon-correct"/>
                &nbsp;
                Correct!
              </h4>
            }
            {this.state.editor.isIncorrect &&
              <h4>
                &nbsp;
                <Glyphicon glyph="remove" className="glyphicon-incorrect"/>
                &nbsp;
                Incorrect!
              </h4>
            }
            <br/><br/>
  	      </div>
  	    }
  	  </div>
    )
  };
};

export default Exercises;