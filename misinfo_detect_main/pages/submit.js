import { useState } from 'react';
import { useRouter } from 'next/router';

export default function SubmitPost() {
    const [content, setContent] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        const token = localStorage.getItem('token');
        if (!token) {
            setError('You must be logged in to post.');
            return;
        }

        const res = await fetch('http://localhost:8080/posts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content }),
        });

        if (res.ok) {
            router.push('/');
        } else {
            setError('Failed to create post.');
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6">Submit New Misinformation</h1>
            <form onSubmit={handleSubmit} className="p-8 bg-white rounded-lg shadow-lg">
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <textarea
                    placeholder="Enter the misinformation content here..."
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    className="w-full p-2 mb-4 border rounded h-40"
                    required
                />
                <button type="submit" className="w-full bg-green-500 hover:bg-green-600 text-white p-2 rounded">Submit Post</button>
            </form>
        </div>
    );
}