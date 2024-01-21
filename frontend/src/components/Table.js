import React, { useEffect } from 'react'
import { useState } from 'react';
import { deleteAlias } from '../ApiFunctions';
import "./Table.css"

export default function Table({ urlData, onDeleteAlias, errorToggle, onError }) {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (urlData && urlData.length > 0) {
            setLoading(false);
        }
    }, [urlData]);

    const handleDelete = (alias) => {
        async function removeAlias() {
            const data = await deleteAlias(alias);
            if (!data.error) {
                onDeleteAlias(alias)
            } else if (data.error && errorToggle) {
                onError("Cannot delete the entry.")
            }
        }
        removeAlias();
    }

    return (
        <div className='tableWrapper'>
            {loading ? (
                <p>Loading.. </p>
            ) : (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Url</th>
                            <th>Alias</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {urlData &&
                            urlData.map((entry, index) => (
                                <tr key={index}>
                                    <td >{entry.url}</td>
                                    <td>{entry.alias}</td>
                                    <td><button onClick={() => handleDelete(entry.alias)}>Delete</button></td>
                                </tr>
                            ))}

                    </tbody>
                </table>
            )}
        </div>
    );
}