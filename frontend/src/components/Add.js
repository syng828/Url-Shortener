import React from 'react'
import { useState } from 'react';
import { addUrl } from '../ApiFunctions';

export default function Add({ onAddUrl }) {

    const [url, setUrl] = useState('');
    const [alias, setAlias] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        async function insertUrl() {
            const url = e.target.elements.url.value;
            const alias = e.target.elements.alias.value;
            let requestBody;
            if (alias === '') {
                requestBody = { "url": url };
            } else {
                requestBody = { "url": url, "alias": alias };
            }
            const data = await addUrl(requestBody);
            if (!data.error) {
                onAddUrl(data.responseData);
            }
        }
        insertUrl();
    }

    return (
        <>
            <div className='Add'>
                <form onSubmit={handleSubmit}>
                    <label htmlFor='url'>Url:</label>
                    <input Url
                        type='text'
                        required
                        value={url}
                        name='url'
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <label htmlFor='alias'>Alias:</label>
                    <input
                        type='text'
                        value={alias}
                        name='alias'
                        onChange={(e) => setAlias(e.target.value)}
                    />
                    <button type='submit'>Add Entry</button>
                </form>
            </div>
        </>
    );
}