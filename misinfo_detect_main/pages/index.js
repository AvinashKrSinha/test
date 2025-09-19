import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Home() {
    const [posts, setPosts] = useState([]);

    const fetchPosts = async () => {
        const res = await fetch('http://localhost:8080/posts/');
        if (res.ok) {
            const data = await res.json();
            setPosts(data);
        }
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    const handleUpvote = async (postId) => {
        const token = localStorage.getItem('token');
        if (!token) {
            alert("Please log in to vote.");
            return;
        }
        const res = await fetch(`http://localhost:8080/posts/${postId}/upvote`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(res.ok) {
            fetchPosts(); // Refresh posts after voting
        }
    };

    return (
        <div className="container mx-auto p-4">
            <nav className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Community Feed</h1>
                <div>
                    <Link href="/submit" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
                        Submit a Post
                    </Link>
                </div>
            </nav>
            <div className="space-y-4">
                {posts.map((post) => (
                    <div key={post.id} className="p-4 border rounded-lg shadow bg-white">
                        <p className="text-gray-800 text-lg">{post.content}</p>
                        <p className="text-sm text-gray-500 mt-2">By: {post.author_email}</p>
                        <div className="flex items-center mt-2">
                            <button onClick={() => handleUpvote(post.id)} className="text-green-500 hover:text-green-700 font-semibold">
                                ▲ Upvote ({post.upvotes})
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}