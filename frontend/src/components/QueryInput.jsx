import { useState } from 'react';

function QueryInput({ onSearch, loading }) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(inputValue);
  };

  return (
    <form onSubmit={handleSubmit} className="query-input-form">
      <div className="input-group">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter your search query..."
          className="query-input"
          disabled={loading}
        />
        <button
          type="submit"
          className="search-button"
          disabled={loading || !inputValue.trim()}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  );
}

export default QueryInput;
