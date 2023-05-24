// CSS files
import './ErrorScreen.css';

function ErrorScreen({errorMessage, setError, setTo}) {
    return (
        <>
            <div className="error-screen">
                <div className="error-div">
                    <h1 className="error-text">{errorMessage}</h1>
                    <button className="error-button" onClick={() => setError(setTo)}>Got it!</button>
                </div>
            </div>
        </>
    )
}

export default ErrorScreen;