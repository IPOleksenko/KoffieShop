import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import MainPage from './js/MainPage';
import reportWebVitals from './test/reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <MainPage />
  </React.StrictMode>
);

reportWebVitals();
