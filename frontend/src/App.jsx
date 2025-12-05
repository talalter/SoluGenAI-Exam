import SearchInterface from './components/SearchInterface';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>RAG Retrieval System</h1>
        <p className="subtitle">By Tal Alter</p>
      </header>

      <main className="app-main">
        <SearchInterface />
      </main>

      <footer className="app-footer">
        <p>Built with FastAPI, React, OpenAI, and ChromaDB</p>
      </footer>
    </div>
  );
}

export default App;
