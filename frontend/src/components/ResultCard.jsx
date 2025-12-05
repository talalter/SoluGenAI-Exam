function ResultCard({ result, rank }) {
  const getScoreColor = (score) => {
    if (score >= 0.8) return '#22c55e'; // green
    if (score >= 0.7) return '#3b82f6'; // blue
    return '#f59e0b'; // orange
  };

  const scorePercentage = (result.similarity_score * 100).toFixed(1);

  return (
    <div className="result-card">
      <div className="result-header">
        <span className="result-rank">#{rank}</span>
        <span
          className="result-score"
          style={{ backgroundColor: getScoreColor(result.similarity_score) }}
        >
          {scorePercentage}% match
        </span>
      </div>

      <div className="result-text">
        {result.text}
      </div>

      <div className="result-metadata">
        <span className="metadata-item">
          Chunk ID: {result.chunk_id.substring(0, 8)}...
        </span>
        <span className="metadata-item">
          Index: {result.chunk_index}
        </span>
      </div>
    </div>
  );
}

export default ResultCard;
