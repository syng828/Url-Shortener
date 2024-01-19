import React, { useEffect } from 'react'
import { useState } from 'react';
import { deleteAlias } from '../ApiFunctions';

export default function Table({ urlData, onDeleteAlias }) {
    const [loading, isLoading] = useState(true);

    useEffect(() => {
        if (urlData && urlData.length > 0) {
            isLoading(false);
        }
    }, [urlData]);

    const handleDelete = (alias) => {
        async function removeAlias() {
            const data = await deleteAlias(alias);
            if (!data.error) {
                onDeleteAlias(alias)
            }
        }
        removeAlias();
    }

    return (
        <><div className='Table'>
            {loading ? (
                <p>Loading.. </p>
            ) : (
                <table>
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
                                    <td>{entry.url}</td>
                                    <td>{entry.alias}</td>
                                    <td><button onClick={() => handleDelete(entry.alias)}>Delete</button></td>
                                </tr>
                            ))}

                    </tbody>
                </table>
            )}
        </div>

        </>
    );
}