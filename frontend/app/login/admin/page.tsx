"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function AdminLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/auth/admin/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        // Clear fields and redirect on successful login
        setEmail('');
        setPassword('');
        
        router.push('/dashboard/admin');
      } else {
        const { message } = await response.json();
        setError(message);
      }
    } catch (err: any) {
      console.error('Error during form submission:', err);
      setError('An error occurred during submission.');
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('/admin.jpg')",  backgroundSize:"75%", backgroundRepeat:"no-repeat", backgroundColor:"white"}}>

      <header className="bg-white shadow-md p-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <img src="/logo.png" alt="Logo" className="h-8" />
        </div>
        <nav className="flex space-x-4">
          <Link href="/home" className="text-gray-800 hover:text-blue-500">Home</Link>
          <Link href="/login/candidate" className="text-gray-800 hover:text-blue-500">Candidates</Link>
          <Link href="/login/educator" className="text-gray-800 hover:text-blue-500">Educators</Link>
          <Link href="/login/admin" className="text-gray-800 hover:text-blue-500">Admins</Link>
        </nav>
      </header>

      <main className="flex-grow flex items-center justify-center">
        <div className="w-full max-w-md p-8 bg-white bg-opacity-90 rounded-lg shadow-lg relative overflow-hidden">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
            Admin Login
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="form-group floating-label-group">
              <input
                id="email"
                type="email"
                placeholder=" "
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field"
                required
              />
              <label htmlFor="email" className="floating-label">
                Email address
              </label>
            </div>
            <div className="form-group floating-label-group">
              <input
                id="password"
                type="password"
                placeholder=" "
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                required
              />
              <label htmlFor="password" className="floating-label">
                Password
              </label>
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button type="submit" className="auth-button">
              Sign in
            </button>
            <p className="text-center text-gray-700 mt-4">
              <Link href="/password-recovery" className="text-blue-500">
                Forgot Password?
              </Link>
            </p>
          </form>
        </div>
      </main>

      <style jsx>{`
        .floating-label-group {
          position: relative;
          margin-top: 1.5rem;
        }

        .input-field {
          width: 100%;
          padding: 1rem 0.75rem;
          border: 1px solid #e5e7eb;
          border-radius: 0.5rem;
          background-color: #f3f4f6;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          transition: border-color 0.3s ease;
          font-size: 1rem;
        }

        .input-field:focus {
          border-color: #4f46e5;
          outline: none;
        }

        .floating-label {
          position: absolute;
          top: 50%;
          left: 0.75rem;
          transform: translateY(-50%);
          background-color: white;
          padding: 0 0.25rem;
          font-size: 0.875rem;
          color: #4f46e5;
          pointer-events: none;
          transition: all 0.3s ease;
          z-index: 1;
        }

        .input-field:focus + .floating-label,
        .input-field:not(:placeholder-shown) + .floating-label {
          top: -0.75rem;
          left: 0.75rem;
          font-size: 0.75rem;
          color: #4f46e5;
        }

        .auth-button {
          width: 100%;
          padding: 0.75rem;
          background-color: #4f46e5;
          color: white;
          border-radius: 0.5rem;
          font-weight: bold;
          cursor: pointer;
          transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .auth-button:hover {
          background-color: #4338ca;
          transform: scale(1.02);
        }
      `}</style>
    </div>
  );
}











