import React from 'react';

function NewPronto() {
    return (
      <div className='newPronto-form-div'>
        <form className='newPronto-form'>
            <label className='newPronto-text-label'>
                <p>First name: </p>
                <input className='newPronto-text-label-input' type = "text" name = "firstName"></input>
            </label>
            <button type="submit">Submit</button>
        </form>
      </div>
    );
  }

export default NewPronto;