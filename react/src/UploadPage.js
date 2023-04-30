import './UploadPage.css';
import fileLogo from './images/File.png';
import close from './images/Close.png';
import MainDiv from './MainDiv';
import uploadicon from './images/upload-icon.png';
import { useRef, useState } from 'react';

function UploadPage({setKey}) {

    setKey('/upload');

    const inputRef = useRef(null);
    const [uploadedFiles, uploadFile] = useState([]);

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
        console.log(event.target.files.length)
        for(let i = 0; i < event.target.files.length; i++) {
            console.log(event.target.files[i]);
            if(!fileUploaded(event.target.files[i])) {
                uploadFile(prevUploadedfiles => [...prevUploadedfiles, event.target.files[i]]);
                console.log(i);
            }
        }
    }

    function fileUploaded(file){
        for(let i = 0; i < uploadedFiles.length; i++) {
            if(uploadedFiles[i].name == file.name)
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

    return(
        <>
            <div className='dropzone-div'>
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
                        </MainDiv>
                    </div>
                )
            }
        </>
    )
}

export default UploadPage;