import { useEffect, useState } from 'react';

import './App.css'

function App() {
    const [message, setMessage] = useState('');

    const apiUrl = import.meta.env.API_URL;

    useEffect(() => {
        fetch(`${apiUrl}`)
        .then(async (res) => {
            const data = await res.json();

            setMessage(data);
        })
        .catch((err) => {
            console.error(err);
        })
    }, [])

    return <h1>{ JSON.stringify(message) }</h1>;
}

export default App
