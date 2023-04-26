import "./NextButton.css";
import { useState } from "react";

const delay = ms => new Promise(
  resolve => setTimeout(resolve, ms)
);

function NextButton({placeholder, text, type, onClick}) {

    const [visibleText, setText] = useState(placeholder);

    const [isHover, setHover] = useState(false);

    const [style, setStyle] = useState({
        borderRadius: "50%",
        padding: "auto auto",
        transition: "1s",
        width: "4vmax"
    })

    async function handleHover() {
        setHover(!isHover);
        if(!isHover) {
            setStyle({
                borderRadius: "40px",
                padding: "20px 20px",
                transition: "0.5s",
                width: text.length*1.75 + "vmax"
            });
            await delay(300);
            let aux = text[0]
            for(let i = 1; i <= text.length; i++) {
                setText(aux);
                aux = aux + text[i];
                await delay(10);
            }
        } else {
            setStyle({
                borderRadius: "50%",
                padding: "0px 0px",
                transition: "0.5s",
                width: "4vmax"
            });
            let aux = text;
            for(let i = 1; i <= text.length; i++) {
                setText(aux);
                aux = aux.slice(0, aux.length-1);
                await delay(20);
            }
            await delay(200);
            setText(placeholder);
        }
    }

    return(
        <button
            className="button"
            onMouseEnter={handleHover}
            onMouseLeave={handleHover}
            style={style}
            type={type}
            onClick={onClick}
        >
            {visibleText}
        </button>
    );
}

export default NextButton