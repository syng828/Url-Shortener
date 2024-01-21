import React from 'react'
import { useState } from 'react';
import { addUrl } from '../ApiFunctions';
import "./Add.css"

export default function Add({ onAddUrl, errorToggle, closeAdd, onError }) {

    const [url, setUrl] = useState('');
    const [alias, setAlias] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        async function insertUrl() {
            const url = e.target.elements.url.value;
            const alias = e.target.elements.alias.value;
            let requestBody;
            const expression = 'https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)';
            const regex = new RegExp(expression);

            try {
                if (!url.match(regex)) {
                    throw new Error('Invalid URL format');
                }

                if (alias === '') {
                    requestBody = { "url": url };
                } else {
                    requestBody = { "url": url, "alias": alias };
                }
                const data = await addUrl(requestBody);
                if (!data.error) {
                    onAddUrl(data.responseData);
                } else if (data.error && errorToggle) {
                    onError("Alias is taken.")
                }
            } catch (error) {
                onError(error.message);
            }
        }
        insertUrl();
    }

    return (
        <div className='add-container' onClick={(e) => {
            if (e.target.className === "add-container")
                closeAdd();
        }}>
            <div className='add'>
                <h3>Add Entry</h3>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor='url'>Url:</label>
                        <input Url
                            type='text'
                            required
                            value={url}
                            name='url'
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor='alias'>Alias:</label>
                        <input
                            type='text'
                            value={alias}
                            name='alias'
                            onChange={(e) => setAlias(e.target.value)}
                        />
                    </div>
                    <button type='submit'>Add Entry</button>
                </form>
            </div >
        </div >
    );
}