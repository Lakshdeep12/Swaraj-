"""
Main React App Component
"""

import React from 'react'
import StressPredictionForm from './StressPredictionForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Stress Detection System</h1>
        <p>Machine Learning-based Stress Prediction</p>
      </header>
      
      <main>
        <StressPredictionForm />
      </main>
      
      <footer className="App-footer">
        <p>© 2026 Stress Detection System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
