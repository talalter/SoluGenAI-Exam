import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryAPI = {
  /**
   * Search for relevant chunks
   * @param {string} query - Search query
   * @returns {Promise} Query results
   */
  async search(query) {
    const response = await api.post('/query', { query });
    return response.data;
  },

  /**
   * Ingest a dataset
   * @param {File} file - CSV file to ingest
   * @returns {Promise} Ingestion results
   */
  async ingest(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/ingest', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default api;
