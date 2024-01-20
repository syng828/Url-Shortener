import React from 'react'
import "./ErrorComponent.css"

export default function ErrorComponent({ message }) {
    console.log(message)
    return (
        <div className="error"
        >
            {message}
        </div>
    )

}