import "./newPronto.css";
import 'react-quill/dist/quill.snow.css';
import MainDiv from './MainDiv';
import ReactQuill from 'react-quill';
import Background from './Background';
import NextButton from './NextButton';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function NewPronto({formData, setFormData}) {

    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
    };

    const [descriere, setDescriere] = useState(formData.descriere);

    function sendDataToFlask() {
      fetch('/receive-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .catch(error => console.error(error));
    }

    const navigate = useNavigate();

    function submitForm() {
      formData.descriere = descriere;
      sendDataToFlask();
      navigate('/result');
    }

    const [left, setLeft] = useState("120vw");

    useEffect(() => {
      setLeft("70vw");
    }, []);

    return (
      <div>
        <Background />
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
        <div style={{left: left, transition: "1s ease", bottom: "5vh", position: "absolute"}}>
          <NextButton placeholder={">"} text={"Continue"} onClick = {submitForm}/>
        </div>
      </div>
    );
  }

export default NewPronto;