import React, { useState, useEffect } from 'react';
import UploadPdfForm from './components/newimg';
import PdfData from './components/display';
import './App.css'
import './index.css';

const App = () => {
  const [isAva,setIsAva] = useState(false);
  return (
    <>
    <h1 className='heading'>Chat Bot</h1>
    <div className='main-container'>
      <UploadPdfForm isAva={isAva} setIsAva={setIsAva}/>
      <div>
        <h3>Ask Question</h3>
      {isAva ? 
        <PdfData  />
        : <></>}
        </div>
        </div>
    </>
  );
};


export default App;