import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import NewPronto from "./newPronto";
import Result from "./Result";
import 'bootstrap/dist/css/bootstrap.min.css';
import Background from './Background';
import Dashboard from './Dashboard';
import UploadPage from './UploadPage';

function App() {

  const [formData, setFormData] = useState({
    titlu: '',
    descriere: '',
    feature: '',
    gic: '',
    release: '',
    state: ''
  });

  const pages = [
    {
      key: '/',
      name: 'Pronto form',
      subpages: []
    },
    {
      key: '/upload',
      name: 'Upload pronto',
      subpages: [
        {
          key: '/',
          name: 'Title 1 ana are mere si alte chestii foarte interesante'
        },
        {
          key: '/',
          name: 'Title 2 ana are'
        }
      ]
    }
  ];

  const [pkey, setKey] = useState('ana');

  return (
    <>
      <Background />
      <Router>
        <Dashboard pages={pages} pkey={pkey}/>
        <Routes>
          <Route path="/" element={<NewPronto formData={formData} setFormData={setFormData} setKey={setKey} />} />
          <Route path="/form-result" element={<Result formData={formData} setKey={setKey} />} />
          <Route path="/upload" element={<UploadPage setKey={setKey} />} />
          {/* <Route path="/upload-result" element={<Result formData={formData} setKey={setKey} />} /> */}
        </Routes>
      </Router>
    </>
  );
}

export default App;