import "./NextButton.css";
import { useState, useEffect } from "react";

function NextButton({placeholder, text, onClick}) {

    const [visibleText, setText] = useState(placeholder);

    const [isHover, setHover] = useState(false);

    const [style, setStyle] = useState({
        borderRadius: "50%",
        padding: "auto auto",
        transition: "1s",
        width: "4vmax"
    })

    useEffect(() => {
        if (isHover) {
          setStyle({
            borderRadius: "40px",
            padding: "20px 20px",
            transition: "0.5s",
            width: (text.length + 2) + "ch"
          });
          delayText();
        } else {
          setStyle({
            borderRadius: "50%",
            padding: "0px 0px",
            transition: "0.5s",
            width: "4vmax"
          });
          resetText();
        }
      }, [isHover]);
    
      async function delayText() {
        await delay(300);
        let aux = text[0];
        for (let i = 1; i <= text.length; i++) {
          setText(aux);
          aux = aux + text[i];
          await delay(10);
          if(!isHover) break;
        }
      }
    
      async function resetText() {
        let aux = text;
        for (let i = 1; i <= text.length; i++) {
          setText(aux);
          aux = aux.slice(0, aux.length - 1);
          await delay(20);
          if(isHover) break;
        }
        await delay(200);
        setText(placeholder);
      }
    
      function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    
      function handleMouseMove() {
        setHover(true);
      }
    
      function handleMouseLeave() {
        setHover(false);
      }

    return(
        <button
            className="button"
            onMouseEnter={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={style}
            onClick={onClick}
        >
            {visibleText}
        </button>
    );
}

export default NextButton