import React from 'react'
import { Link } from 'react-router-dom'

export default function Nav() {
    return (
        <div className='navbar'>
            <Link to='/'><button>Home</button></Link>
            <Link to='/add'><button>Add URL</button></Link>
            <Link to='/delete'><button>Delete URL</button></Link>
        </div>
    )
}
