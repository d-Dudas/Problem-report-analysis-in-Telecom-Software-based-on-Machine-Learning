import { useNavigate } from 'react-router-dom';
import "./newPronto.css";
import Background from './Background';
import NextButton from './NextButton';
import MainDiv from './MainDiv';

function NewPronto({formData, setFormData}) {

    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
    };

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

    const handleSubmit = (event) => {
      event.preventDefault();
      sendDataToFlask();
      navigate('/result');
    };

    function submitForm() {
      sendDataToFlask();
      navigate('/result');
    }

    return (
      <div>
        <Background />
        <div className='header'></div>
        <MainDiv headerText="Upload new pronto">
          <form className='newPronto-form' onSubmit={handleSubmit}>
              <label className='newPronto-text-label'>
                  <p>Titlu: </p>
                  <input className='newPronto-text-label-input' type = "text" name = "titlu" value={formData.titlu} onChange={handleChange} ></input>
              </label>
              <label className='newPronto-text-label'>
                  <p>Feature: </p>
                  <input className='newPronto-text-label-input' type = "text" name = "feature" value={formData.feature} onChange={handleChange}></input>
              </label>
              <label className='newPronto-text-label'>
                  <p>Group in charge: </p>
                  <input className='newPronto-text-label-input' type = "text" name = "gic" value={formData.gic} onChange={handleChange}></input>
              </label>
              <label className='newPronto-text-label'>
                  <p>Release: </p>
                  <input className='newPronto-text-label-input' type = "text" name = "release" value={formData.release} onChange={handleChange}></input>
              </label>
              <label className='newPronto-text-label'>
                  <p>Descriere: </p>
                  <textarea className='newPronto-descriere newPronto-text-label-input' rows={10} name = "descriere" value={formData.descriere} onChange={handleChange}></textarea>
              </label>
          </form>
        </MainDiv>
        <NextButton placeholder={">"} text={"Continue"} type={"submit"} onClick = {submitForm}/>
        <div className='footer'></div>
      </div>
    );
  }

export default NewPronto;