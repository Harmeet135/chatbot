import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PdfData = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleQuestionChange = (event) => {
        setQuestion(event.target.value);
    };

    const askQuestion = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('http://127.0.0.1:8000/ask', { question });
            setAnswer(response.data.answer); 
            setLoading(false);
        } catch (error) {
            setError('An error occurred while fetching the answer');
            setLoading(false);
        }
    };

    return (
        <div>
            <div>
                <input
                    type="text"
                    value={question}
                    onChange={handleQuestionChange}
                    placeholder="Ask a question..."
                />
                <button onClick={askQuestion} disabled={loading}>
                    Ask
                </button>
            </div>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {answer && !loading && (
                <div>
                    <p><strong>Answer:</strong> {answer}</p>
                </div>
            )}
        </div>
    );
};

export default PdfData;
