import React from 'react';
import './FormErrors.css';

const FormErrors = (props) => {
  return (
    <div>
      <ul className="validation-list">
        {
          props.formRules.map((rule) => {
          	return (
          	  <li key={rule.id} className={rule.valid ? "success" : "error"}>
          	    {rule.name}
          	  </li>
          	)
          })
        }
      </ul>
    </div>
  )
};

export default FormErrors;