import React, { useState } from 'react';
import axios from 'axios';

const UploadPdfForm = ({isAva,setIsAva}) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('pdf', file);

        try {
            const response = await axios.post('http://127.0.0.1:8000/', formData);

            if (response.status === 201) {
                setIsAva(!isAva)
                setMessage('PDF uploaded successfully');
            } else {
                setMessage('Failed to upload PDF');
            }
        } catch (error) {
            setMessage('An error occurred while uploading PDF');
        }
    };

    return (
        <div>
            <h2>Upload PDF</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="pdf">Select PDF file:</label>
                    <input type="file" id="pdf" onChange={handleFileChange} accept=".pdf" />
                </div>
                <button type="submit">Upload</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default UploadPdfForm;
