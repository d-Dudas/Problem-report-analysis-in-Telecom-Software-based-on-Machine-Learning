import "./newPronto.css";
import 'react-quill/dist/quill.snow.css';
import MainDiv from './MainDiv';
import ReactQuill from 'react-quill';
import NextButton from './NextButton';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function NewPronto({formData, setFormData, setKey}) {

  setKey('/');

    function sendDataToFlask() {
      fetch('/receive-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
        setFormData({ ...formData, state: data.msg });
      })
      .catch(error => console.error(error));
    }
    
    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
    };

    const [descriere, setDescriere] = useState(formData.descriere);

    const navigate = useNavigate();

    function submitForm() {
      formData.descriere = descriere;
      formData.state = "abc";
      if(Object.keys(formData).filter(key => key !== "state").some(key => formData[key] === null || formData[key] === '' || formData[key] === undefined)) {
        console.log("Nem jo.");
      } else {
        formData.state = '';
        sendDataToFlask();
        navigate('/form-result');
      }
    }

    // By default, put the element out of the screen
    const [left, setLeft] = useState("120vw");

    // When page starts, put the element on place
    useEffect(() => {
      setLeft("77vw");
    }, []);

    return (
      <div>
        <div class='newPronto-div'>
          <MainDiv headerText="Upload new pronto">
            <form className='newPronto-form'>
                <label className='newPronto-text-label'>
                    <p>Titlu</p>
                    <input className='newPronto-text-label-input' placeholder='Titlu' type = "text" name = "titlu" value={formData.titlu} onChange={handleChange} ></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Feature</p>
                    <input className='newPronto-text-label-input' placeholder='Feature' type = "text" name = "feature" value={formData.feature} onChange={handleChange}></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Group in charge</p>
                    <input className='newPronto-text-label-input' placeholder='Group in charge' type = "text" name = "gic" value={formData.gic} onChange={handleChange}></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Release</p>
                    <input className='newPronto-text-label-input' placeholder='Release' type = "text" name = "release" value={formData.release} onChange={handleChange}></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Descriere</p>
                    <ReactQuill placeholder='Descriere' className='newPronto-descriere' theme="snow" name = "descriere" value={descriere} onChange={setDescriere}/>
                </label>
            </form>
          </MainDiv>
        </div>
        <div style={{left: left, transition: "1s ease", bottom: "5vh", position: "absolute"}}>
          <NextButton placeholder={">"} text={"Continue"} onClick = {submitForm}/>
        </div>
      </div>
    );
  }

export default NewPronto;