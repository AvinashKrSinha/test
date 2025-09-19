import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        const formData = new URLSearchParams({ username, password });
        const res = await fetch('http://localhost:8080/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('token', data.access_token);
            router.push('/');
        } else {
            setError('Login failed. Check your credentials.');
        }
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-50">
            <form onSubmit={handleSubmit} className="p-8 bg-white rounded-lg shadow-lg w-96">
                <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <input type="email" placeholder="Email" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-2 mb-4 border rounded"/>
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-2 mb-4 border rounded"/>
                <button type="submit" className="w-full bg-blue-500 hover:bg-blue-600 text-white p-2 rounded">Login</button>
            </form>
        </div>
    );
}