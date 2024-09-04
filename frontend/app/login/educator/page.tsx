"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import { useRouter } from 'next/navigation';

interface FormData {
  email: string;
  password: string;
}

export default function EducatorLogin() {
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const validationSchema = Yup.object().shape({
    email: Yup.string().email('Invalid email address').required('Email is required'),
    password: Yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
  });

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: yupResolver(validationSchema),
  });

  const onSubmit = async (data: FormData) => {
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorDetails = await response.json();
        throw new Error(errorDetails.message || 'An error occurred during submission.');
      }

      const responseData = await response.json();
      localStorage.setItem('token', responseData.access_token);
      console.log('Login successful:', responseData);
      router.push('/dashboard/educator');
    } catch (err: any) {
      console.error('Error during form submission:', err);
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
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

      <main className="flex-grow flex items-center justify-center bg-cover bg-center" style={{ backgroundImage: "url('/educ.jpg')" , backgroundSize:"75%", backgroundRepeat:"no-repeat", backgroundColor:"white"}}>
        <div className="w-full max-w-md p-8 bg-white bg-opacity-90 rounded-lg shadow-lg relative overflow-hidden">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Educator Login</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="form-group floating-label-group">
              <input
                {...register('email')}
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="input-field"
                placeholder=" "
              />
              <label htmlFor="email" className="floating-label">
                Email address
              </label>
              {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email?.message}</p>}
            </div>

            <div className="form-group floating-label-group">
              <input
                {...register('password')}
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="input-field"
                placeholder=" "
              />
              <label htmlFor="password" className="floating-label">
                Password
              </label>
              {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password?.message}</p>}
            </div>

            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

            <button type="submit" className="auth-button">
              Sign in
            </button>

            <Link href="/password-recovery" className="text-blue-500 text-center block mt-4">
              Forgot Password?
            </Link>
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








