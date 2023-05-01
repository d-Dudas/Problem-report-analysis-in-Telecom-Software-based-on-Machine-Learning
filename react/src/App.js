import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import NewPronto from "./newPronto";
import Result from "./Result";
import 'bootstrap/dist/css/bootstrap.min.css';
import Background from './Background';
import Dashboard from './Dashboard';
import UploadPage from './UploadPage';
import './variables.css';

function App() {

  const [formData, setFormData] = useState({
    titlu: '',
    descriere: '',
    feature: '',
    gic: '',
    release: '',
    state: ''
  });

  const [prontoList, setProntoList] = useState([])

  const [pages, setPages] = useState([
    {
      key: '/',
      name: 'Pronto form',
      subpages: []
    },
    {
      key: '/upload',
      name: 'Upload pronto',
      subpages: []
    }
  ]);

  const [pkey, setKey] = useState('ana');

  return (
    <>
      <Background />
      <Router>
        <Dashboard pages={pages} pkey={pkey}/>
        <Routes>
          <Route path="/" element={<NewPronto formData={formData} setFormData={setFormData} setKey={setKey} />} />
          <Route path="/form-result" element={<Result formData={formData} setKey={setKey} pkey={"/"}/>} />
          <Route path="/upload" element={<UploadPage setKey={setKey} dashboard_content={pages} setDash={setPages} setProntoList={setProntoList}/>} />
          {prontoList.map(pronto => {
            return(<Route path={"/" + pronto.problemReportId} element={<Result formData={pronto} setKey={setKey} pkey={"/" + pronto.problemReportId}/>} />);
          })}
        </Routes>
      </Router>
    </>
  );
}

export default App;