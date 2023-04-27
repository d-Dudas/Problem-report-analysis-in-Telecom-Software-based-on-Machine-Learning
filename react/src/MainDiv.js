import "./MainDiv.css";
import React from "react";

function MainDiv(props) {
    return(
        <div className='main-div'>
            <div className='main-header-div'>
                <h1 className='main-header-text'>{props.headerText}</h1>
            </div>
            {props.children}
        </div>
    );
}

export default MainDiv;