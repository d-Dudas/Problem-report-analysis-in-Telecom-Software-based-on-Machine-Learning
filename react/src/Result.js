import './newPronto.css';
import "./Result.css";
import MainDiv from './MainDiv';
import parse from 'html-react-parser'
import Background from './Background';
import NextButton from './NextButton';
import { useNavigate } from 'react-router-dom';

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
                <p><strong>Titlu:</strong> {formData.titlu}</p>
                <p><strong>Feature:</strong> {formData.feature}</p>
                <p><strong>Release:</strong> {formData.release}</p>
                <p><strong>Gic:</strong> {formData.gic}</p>
                <p><strong>Descriere:</strong></p>{parse(formData.descriere)}
            </div>
        </MainDiv>
        <NextButton placeholder={"<"} text={"Back"} type={"submit"} onClick = {switchPage}/>
        <div className='footer'></div>
      </div>
    );
}

export default Result;