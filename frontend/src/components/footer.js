import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
    const year = new Date().getFullYear()
    return (
        <footer className="bg-dark text-center text-white">
            <div className="text-center p-3" style={{backgroundColor: "rgba(0, 0, 0, 0.2)"}}>
                © {year} Copyright:&nbsp;
                <Link className="text-white" to='/'>Product Hunt</Link>
            </div>
        </footer>
    )
}
