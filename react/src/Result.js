import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function Result({formData}){
    const navigate = useNavigate();

    function switchPage () 
    {  
      navigate('/');
    }

    return(
        <div className='d-flex justify-content-center align-items-center'>
            <div>
                <h1>Current form data:</h1>
                <p>Titlu: {formData.titlu}</p>
                <p>Feature: {formData.feature}</p>
                <p>Release: {formData.Release}</p>
                <p>Gic: {formData.gic}</p>
                <p>Descriere: {formData.descriere}</p>
            </div>
            <button onClick={switchPage}>Home</button>
        </div>
    );
}

export default Result;