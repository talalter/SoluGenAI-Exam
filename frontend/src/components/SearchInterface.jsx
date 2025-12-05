import { useState } from 'react';
import { queryAPI } from '../services/api';
import QueryInput from './QueryInput';
import ResultCard from './ResultCard';

function SearchInterface() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await queryAPI.search(searchQuery);
      setResults(data.results);
      setQuery(searchQuery);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to search. Please try again.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-interface">
      <QueryInput onSearch={handleSearch} loading={loading} />

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          Searching...
        </div>
      )}

      {!loading && results.length === 0 && query && !error && (
        <div className="no-results">
          No results found for "{query}"
        </div>
      )}

      {!loading && results.length > 0 && (
        <div className="results-container">
          <h2>Found {results.length} results for "{query}"</h2>
          <div className="results-list">
            {results.map((result, index) => (
              <ResultCard key={result.chunk_id} result={result} rank={index + 1} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default SearchInterface;
