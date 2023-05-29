// CSS files
import "./newPronto.css";
import 'react-quill/dist/quill.snow.css';

// Components
import MainDiv from './MainDiv';
import ReactQuill from 'react-quill';
import NextButton from './NextButton';
import LoadingScreen from "./LoadingScreen";
import ErrorScreen from "./ErrorScreen";

// Images, icons
import addIcon from './images/Add.png'
import removeList from './images/remove.png'
import downIcon from './images/downIcon.png'

// React related
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function NewPronto({setKey, dashboard_content, setDash, setProntoList, prontoList}) {
  
    setKey('/');

    const [formData, setFormData] = useState({
      problemReportId: '',
      title: '',
      description: '',
      feature: '',
      groupInCharge: '',
      release: "",
      state: '',
      saved: false,
      faultAnalysisId: [],
      attachedPRs: [],
      author: "",
      build: "",
      authorGroup: "",
      informationrequestID: [],
      statusLog: "",
      explanationforCorrectionNotNeeded: [],
      reasonWhyCorrectionisNotNeeded: [],
      faultAnalysisFeature: [],
      faultAnalysisGroupInCharge: [],
      stateChangedtoClosed: [],
      faultAnalysisTitle: []
    });

    const auxProntoList = prontoList.slice();
    const [descriere, setDescriere] = useState(formData.descriere);
    const navigate = useNavigate();
    const [error, setError] = useState(false);
    const [loading, setloading] = useState(false);
    const mandatoryFields = ["description", "title"];
    const [showOptional, setShowOptional] = useState(false);

    function sendDataToFlask() {
      setloading(true);
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

        // Rebuild the subpages list
        let name = data.title;
        let key = "/" + name;
        dashboard_content[0].subpages.push({key: key, name: name});

        setProntoList(auxProntoList);
        setDash(dashboard_content);
        navigate('/' + auxProntoList[auxProntoList.length-1].title);
      })
      .catch(error => console.error(error));
    }
    
    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
    };

    function submitForm() {
      formData.description = descriere;
      formData.release = [formData.release];
      let err = false
      for(let i = 0; i < mandatoryFields.length; i++) {
        let key = mandatoryFields[i];
        if(Array.isArray(formData[key])) {
          if(formData[key].length <= 1 && formData[key][0] === "")
            err = true;
        } else {
          if(formData[key] === null || formData[key] === '' || formData[key] === undefined)
            err = true;
        }
      }
      if(err) {
        setError(true);
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

    function handleAddList(event) {
      const {name} = event.target;
      let aux = formData[name].slice();
      if(!aux.some(value => value === "" || value === null || value === undefined)) {
        aux.push("");
        setFormData({...formData, [name]: aux});
      }
    }

    function handleListValue(index, event) {
      const {name, value} = event.target;
      let aux = formData[name].slice();
      aux[index] = value;
      setFormData({...formData, [name]: aux});
    }

    function handleRemoveList(index, event) {
      const {name} = event.target;
      let aux = formData[name].slice();
      aux.splice(index, 1);
      setFormData({...formData, [name]: aux});
    }

    function handleOptionalFields() {
      setShowOptional(!showOptional);
    }

    function listInput(list) {
      return (
              <>
                <label className='newPronto-list-label'>
                  <p>{list}</p>
                  <img src={addIcon} alt="" className="newPronto-list-add-button" name={list} onClick={handleAddList}></img>
                </label>
                {
                  formData[list].map((element, index) => (
                    <label>
                      <input type="text"
                              name={list}
                              value={element}
                              className='newPronto-text-label-input'
                              placeholder={list}
                              style={{margin: "10px 0px", width: "90%"}}
                              onChange={(event) => handleListValue(index, event)}
                      />
                      <img src={removeList} alt='' className="newPronto-list-remove-button" name={list} onClick={(event) => handleRemoveList(index, event)}></img>
                    </label>
                  ))
                }
              </>
      )
    }

    const optionalFields = () => {
      return (
          <div>
          <label className='newPronto-text-label'>
              <p>Author</p>
              <input className='newPronto-text-label-input' placeholder='Author' type = "text" name = "author" value={formData.author} onChange={handleChange}></input>
          </label>
          <label className='newPronto-text-label'>
              <p>Author group</p>
              <input className='newPronto-text-label-input' placeholder='Author group' type = "text" name = "authorGroup" value={formData.authorGroup} onChange={handleChange}></input>
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
              <p>Build</p>
              <input className='newPronto-text-label-input' placeholder='Build' type = "text" name = "build" value={formData.build} onChange={handleChange}></input>
          </label>
          <label className='newPronto-text-label'>
              <p>Status log</p>
              <input className='newPronto-text-label-input' placeholder='Status log' type = "text" name = "statusLog" value={formData.statusLog} onChange={handleChange}></input>
          </label>
          {listInput("faultAnalysisId")}
          {listInput("attachedPRs")}
          {listInput("informationrequestID")}
          {listInput("explanationforCorrectionNotNeeded")}
          {listInput("reasonWhyCorrectionisNotNeeded")}
          {listInput("faultAnalysisFeature")}
          {listInput("faultAnalysisGroupInCharge")}
          {listInput("stateChangedtoClosed")}
          {listInput("faultAnalysisTitle")}
        </div>
      )
    }

    return (
      <div>
        {loading ? <LoadingScreen /> : null}
        {error ?
          <ErrorScreen errorMessage={"Title and description are mandatory"} setError={setError} setTo={false} /> : null
        }
        <div class='newPronto-div'>
          <MainDiv headerText="Get new prediction" result={false}>
            <form className='newPronto-form' style={!showOptional ? {top: "10%"} : null}>
                <label className='newPronto-text-label'>
                    <p>Title</p>
                    <input className='newPronto-text-label-input' placeholder='Title' type = "text" name = "title" value={formData.title} onChange={handleChange} ></input>
                </label>
                <label className='newPronto-text-label'>
                    <p>Description</p>
                    <ReactQuill placeholder='Description' className='newPronto-descriere' theme="snow" name = "descriere" value={descriere} onChange={setDescriere}/>
                </label>
                <div className="newPronto-showOptional-div">
                  <p className="newPronto-showOptional-text">{showOptional ? "Hide" : "Show"} optional fields</p>
                  <img src={downIcon} alt='' className="newPronto-showOptional-button" onClick={handleOptionalFields} style={showOptional ? {rotate: "180deg", transform: "translateX(50%)"} : {rotate: "0deg", transform: "translateX(-50%)"}}></img>
                </div>
                {showOptional ? optionalFields() : null}
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