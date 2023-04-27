import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import NewPronto from "./newPronto";
import Result from "./Result";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [formData, setFormData] = useState({
    titlu: '',
    descriere: '',
    feature: '',
    gic: '',
    release: ''
  });

  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewPronto formData={formData} setFormData={setFormData} />} />
        <Route path="/result" element={<Result formData={formData} />} />
      </Routes>
    </Router>
  );
}

export default App;