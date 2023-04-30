import './newPronto.css';
import "./Result.css";
import MainDiv from './MainDiv';
import parse from 'html-react-parser'
import NextButton from './NextButton';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect} from 'react';
import LoadingDots from './LoadingDots';

function Result({formData, setKey}){

  setKey('/upload');

    const navigate = useNavigate();

    function switchPage () 
    {  
      navigate('/');
    }

    const [left, setLeft] = useState("120vw");

    useEffect(() => {
      setLeft("70vw");
    }, []);

    return(
        <div>
        <div className='header'></div>
        <MainDiv headerText={"Prediction"}>
            <div className='result-div'>
                <p><strong>Titlu:</strong> {formData.titlu}</p>
                <p><strong>Feature:</strong> {formData.feature}</p>
                <p><strong>Release:</strong> {formData.release}</p>
                <p><strong>Gic:</strong> {formData.gic}</p>
                <p><strong>Descriere:</strong></p>{parse(formData.descriere)}
                <div className='result'><p><strong>Predicted state:</strong></p> {formData.state === '' ? <LoadingDots /> : <p>{formData.state}</p>}</div>
            </div>
        </MainDiv>
        <div style={{left: left, transition: "1s ease", bottom: "5vh", position: "absolute"}}>
          <NextButton placeholder={"<"} text={"Back"} type={"submit"} onClick = {switchPage}/>
        </div>
        <div className='footer'></div>
      </div>
    );
}

export default Result;