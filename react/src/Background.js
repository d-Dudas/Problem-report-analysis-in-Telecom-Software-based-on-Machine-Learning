import "./Background.css";
import logo from "./images/Nokia.png";

function Background()
{
    return(
        <div className="background">
            <div className="background-header">
                <img src={logo} alt="" className="background-header-logo"></img>
            </div>
            <div className="background-object">
                <div className="background-object-polygon"></div>
            </div>
            <div className="background-footer"></div>
        </div>
    );
}

export default Background