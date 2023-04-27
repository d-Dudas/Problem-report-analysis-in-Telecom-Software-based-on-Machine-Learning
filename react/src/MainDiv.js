import "./MainDiv.css";
import React, { useState, useRef, useEffect } from "react";

function MainDiv(props) {

    const [top, setTop] = useState("-100vh");

    const divRef = useRef(null);

    useEffect(() => {
        // Keep the scroll at the bottom of the div
        divRef.current.scrollTop = divRef.current.scrollHeight;
    }, [divRef.current?.scrollHeight]);

    useEffect(() => {
        setTop("10vh");
      }, []);

    return(
        <div className='main-div' style={{top: top}}>
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