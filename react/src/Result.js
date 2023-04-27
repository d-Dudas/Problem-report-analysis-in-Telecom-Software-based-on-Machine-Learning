import { useNavigate } from 'react-router-dom';
import './newPronto.css';
import "./Result.css";
import Background from './Background';
import NextButton from './NextButton';
import MainDiv from './MainDiv';

function Result({formData}){
    const navigate = useNavigate();

    function switchPage () 
    {  
      navigate('/');
    }

    return(
        <div>
        <Background />
        <div className='header'></div>
        <MainDiv headerText={"Prediction"}>
            <div className='result-div'>
                <h1>Current form data:</h1>
                <p>Titlu: {formData.titlu}</p>
                <p>Feature: {formData.feature}</p>
                <p>Release: {formData.release}</p>
                <p>Gic: {formData.gic}</p>
                <p>Descriere: {formData.descriere}</p>
            </div>
        </MainDiv>
        <NextButton placeholder={"<"} text={"Back"} type={"submit"} onClick = {switchPage}/>
        <div className='footer'></div>
      </div>
    );
}

export default Result;