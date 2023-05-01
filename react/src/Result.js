import './newPronto.css';
import "./Result.css";
import MainDiv from './MainDiv';
import parse from 'html-react-parser'
import NextButton from './NextButton';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect} from 'react';
import LoadingDots from './LoadingDots';
import { Chart } from "react-google-charts";

function Result({formData, setKey, pkey}){

  setKey(pkey);

    const navigate = useNavigate();

    function switchPage () 
    {  
      navigate('/');
    }

    const [left, setLeft] = useState("120vw");

    useEffect(() => {
      setLeft("70vw");
    }, []);

    const data = [
      ["Task", "Hours per Day"],
      ["", 73.6],
      ["", (100 - 73.6)]
    ];
    
    const options = {
      title: "",
      is3D: false,
      pieHole: 0.8,
      legend: "none",
      pieSliceText: "none",
      slices: {
        0: { color: "rgb(66, 167, 255)" },
        1: { color: "transparent" },
      },
    };

    return(
      <div className='result-content'>
        <div className='main-div-result'>
          <MainDiv headerText={"Prediction"}>
              <div className='result-div'>
                  <p><strong>Titlu:</strong> {formData.title}</p>
                  <p><strong>Feature:</strong> {formData.feature}</p>
                  <p><strong>Release:</strong> {formData.release}</p>
                  <p><strong>Gic:</strong> {formData.gic}</p>
                  <p><strong>Descriere:</strong></p>{parse(formData.descriere)}
                  <div className='result'><p><strong>Predicted state:</strong></p> {formData.state === '' ? <LoadingDots /> : <p>{formData.state}</p>}</div>
              </div>
          </MainDiv>
        </div>
        <div className='save-pronto-div'>
          <MainDiv headerText={"Accuracy"}>
            <p className='accuracy-text1'>Our machine learnig model currently has a prediction accuracy of:</p>
            <div className='d-chart'>
            <Chart
              chartType="PieChart"
              data={data}
              options={options}
              width={"100%"}
              height={"30vh"}
            />
            </div>
          </MainDiv>
        </div>
      </div>
    );
}

export default Result;