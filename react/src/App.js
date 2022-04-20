import MiniDrawer from './components/MiniDrawer';
import { Routes, Route, Link } from "react-router-dom";
import './App.css';
import IntroConfig from './components/IntroConfig';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<IntroConfig />} />
        <Route path="analyze" element={<MiniDrawer />} />
      </Routes>
    </div>
  );
}

export default App;
