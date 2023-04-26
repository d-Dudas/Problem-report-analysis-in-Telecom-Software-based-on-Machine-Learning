import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage({formData}) {
    const navigate = useNavigate();

    function switchPage () 
    {  
      navigate('/form');
    }

    return (
        <div className='homePage-div'>
          <button className='newProntoButton' onClick={switchPage}>Upload new pronto</button>
        </div>
    );
}

export default HomePage;