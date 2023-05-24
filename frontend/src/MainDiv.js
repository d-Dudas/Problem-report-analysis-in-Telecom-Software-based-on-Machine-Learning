// CSS files
import "./MainDiv.css";

// React related
import React, { useRef, useEffect } from "react";

function MainDiv(props) {

    const divRef = useRef(null);

    useEffect(() => {
        // Keep the scroll at the bottom of the div
        if(props.result)
            divRef.current.scrollTop = divRef.current.scrollHeight;
    }, [divRef.current?.scrollHeight, props.result]);

    return(
        <div className='main-div'>
            <div className='main-header-div'>
                <h1 className='main-header-text'>{props.headerText}</h1>
            </div>
            <div ref={divRef} className="main-content-div">
                {props.children}
            </div>
        </div>
    );
}

export default MainDiv;