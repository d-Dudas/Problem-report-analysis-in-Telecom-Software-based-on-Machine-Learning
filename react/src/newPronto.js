// CSS files
import "./newPronto.css";
import 'react-quill/dist/quill.snow.css';

// Components
import MainDiv from './MainDiv';
import ReactQuill from 'react-quill';
import NextButton from './NextButton';

// React related
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function NewPronto({setKey, dashboard_content, setDash, setProntoList, prontoList}) {
  
    setKey('/');

    const [formData, setFormData] = useState({
      problemReportId: '123',
      title: '',
      description: '',
      feature: '',
      groupInCharge: '',
      release: '',
      state: '',
      saved: false
    });

    const auxProntoList = prontoList.slice();
    const [descriere, setDescriere] = useState(formData.descriere);
    const navigate = useNavigate();

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
        auxProntoList.push(data);
        setProntoList(auxProntoList);
        console.log(auxProntoList);

        // Rebuild the subpages list
        let key = "/" + data.problemReportId;
        let name = data.problemReportId;
        console.log(dashboard_content);
        dashboard_content[0].subpages.push({key: key, name: name});

        setProntoList(auxProntoList);
        setDash(dashboard_content);
        navigate('/' + auxProntoList[auxProntoList.length-1].problemReportId);
      })
      .catch(error => console.error(error));
    }
    
    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
    };

    function submitForm() {
      formData.description = descriere;
      if(Object.keys(formData).filter(key => key !== "state" && key !== "saved").some(key => formData[key] === null || formData[key] === '' || formData[key] === undefined)) {
        console.log("Nem jo.");
      } else {
        formData.state = '';
        sendDataToFlask();
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
                    <input className='newPronto-text-label-input' placeholder='Titlu' type = "text" name = "title" value={formData.titlu} onChange={handleChange} ></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Feature</p>
                    <input className='newPronto-text-label-input' placeholder='Feature' type = "text" name = "feature" value={formData.feature} onChange={handleChange}></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Group in charge</p>
                    <input className='newPronto-text-label-input' placeholder='Group in charge' type = "text" name = "groupInCharge" value={formData.gic} onChange={handleChange}></input>
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