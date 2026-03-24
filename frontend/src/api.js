import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const submitLead = async (leadData) => {
    try {
        const response = await axios.post(`${API_URL}/lead`, leadData);
        return response.data;
    } catch (error) {
        console.error("Error submitting lead:", error);
        throw error;
    }
};

export const checkHealth = async () => {
    try {
        const response = await axios.get(`${API_URL}/health`);
        return response.data;
    } catch (error) {
        console.error("Error checking health:", error);
        throw error;
    }
};
