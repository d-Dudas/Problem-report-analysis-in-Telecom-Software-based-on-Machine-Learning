// Css files
import './UploadPage.css';

// Images, icons
import fileLogo from './images/json-logo.png';
import uploadicon from './images/upload-icon.png';
import close from './images/Close.png';

// Components
import MainDiv from './MainDiv';
import NextButton from './NextButton';

// React related
import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UploadPage({setKey, dashboard_content, setDash, setProntoList, prontoList}) {

    setKey('/upload');

    const inputRef = useRef(null);
    const navigate = useNavigate();
    const [uploadedFiles, uploadFile] = useState([]);
    const auxProntoList = prontoList.slice();

    function handleDragOver(event) {
        event.preventDefault();
    }

    function handleDrop(event) {
        event.preventDefault();
        for(let i = 0; i < event.dataTransfer.files.length; i++) {
            if(!fileUploaded(event.dataTransfer.files[i]))
                uploadFile([...uploadedFiles, event.dataTransfer.files[i]]);
        }
    }

    function handleInput(event) {
        for(let i = 0; i < event.target.files.length; i++) {
            if(!fileUploaded(event.target.files[i])) {
                uploadFile(prevUploadedfiles => [...prevUploadedfiles, event.target.files[i]]);
            }
        }
    }

    function fileUploaded(file){
        for(let i = 0; i < uploadedFiles.length; i++) {
            if(uploadedFiles[i].name === file.name)
                return(true);
        }
        return(false);
    }

    function removeFile(event){
        let name = event.target.getAttribute("fname");
        uploadFile(oldFiles => {
            return oldFiles.filter(f => f.name !== name)
        })
    }

    function notInProntoList(pronto) {
        for(let i = 0; i < auxProntoList.length; i++) {
            if(auxProntoList[i].problemReportId === pronto.problemReportId)
                return(false);
        }
        return(true);
    }

    function notInSubpagesList(pronto) {
        for(let i = 0; i < dashboard_content[1].subpages.length; i++) {
            if(dashboard_content[1].subpages[i].key === pronto.key)
                return(false);
        }
        return(true);
    }

    function setSubpages(data) {
        // Push the new prontos in auxiliar pronto list
        for(let i = 0; i < data.length; i++) {
            if(notInProntoList(data[i]))
                auxProntoList.push(data[i]);
        }

        // Rebuild the subpages list
        let subpages = dashboard_content[1].subpages;
        for(let i = 0; i < data.length; i++) {
            let key = "/" + data[i].problemReportId;
            let name = data[i].problemReportId;
            if(notInSubpagesList({key: key, name: name}))
                subpages.push({key: key, name: name})
        }

        dashboard_content[1].subpages = subpages;
        setProntoList(auxProntoList);
        setDash(dashboard_content);

        // Go to the most recently addded pronto
        navigate('/' + auxProntoList[auxProntoList.length-1].problemReportId);
    }

    async function uploadFiles() {
        const formData = new FormData();
        for(let i = 0; i < uploadedFiles.length; i++){
            formData.append('files[]', uploadedFiles[i]);
        }

        try {
            const response = await fetch('/receive-files', {
              method: 'POST',
              body: formData,
            });
            const data = await response.json();
            setSubpages(data);
          } catch (error) {
            console.error(error);
          }
    }

    return(
        <div className='upload-page-content'>
            <div className={uploadedFiles.length > 0 ? 'dropzone-div' : 'dropzone-div-alone'}>
                <MainDiv headerText="Upload new pronto">
                    <div 
                        className='dropzone'
                        onDragOver={handleDragOver}
                        onDrop={handleDrop}
                    >
                        <img className='upload-icon' src={uploadicon} alt='' onClick={() => inputRef.current.click()}></img>
                        <h1 className='upload-text' onClick={() => inputRef.current.click()}>Upload pronto files (JSON)</h1>
                        <input 
                            type='file'
                            multiple
                            onChange={handleInput}
                            hidden
                            accept='.json'
                            ref={inputRef}
                        />
                    </div>
                </MainDiv>
            </div>
            {
                uploadedFiles.length > 0 && (
                    <div className='files'>
                        <MainDiv headerText='Prontos'>
                            <div className='files-list'>
                                {uploadedFiles.map(file => {
                                        return(
                                            <div className='uploaded-file-div'>
                                                <img src={fileLogo} alt='' className='uploaded-file-logo'></img>
                                                <h1 className='uploaded-file-text'>{file.name}</h1>
                                                <img src={close} alt='' className='uploaded-file-close' fname={file.name} onClick={removeFile}></img>
                                            </div>
                                        )
                                })}
                            </div>
                            <div className='upload-files-button'>
                                <NextButton placeholder={">"} text={"Upload"} onClick={uploadFiles}/>
                            </div>
                        </MainDiv>
                    </div>
                )
            }
        </div>
    )
}

export default UploadPage;