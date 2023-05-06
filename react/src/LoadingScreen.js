// CSS files
import './LoadingScreen.css'

// Components
import LoadingDots from './LoadingDots';

function LoadingScreen() {
    return(
        <>
            <div className='loading-screen-background'>
                <div className='loading-screen-animation'>
                    <LoadingDots />
                </div>
            </div>
        </>
    );
}

export default LoadingScreen;