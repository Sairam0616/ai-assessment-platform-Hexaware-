"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import { useRouter } from 'next/navigation';

interface FormData {
  username?: string;
  email: string;
  password: string;
}

export default function RegisterLogin() {
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const validationSchema = Yup.object().shape({
    username: isRegistering ? Yup.string().required('Username is required') : Yup.string(),
    email: Yup.string().email('Invalid email address').required('Email is required'),
    password: Yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
  });

  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
    resolver: yupResolver(validationSchema),
  });
  const onSubmit = async (data: FormData) => {
    setError(null);

    try {
        const endpoint = isRegistering ? '/auth/candidate/register' : '/auth/candidate/login';
        const response = await fetch(`http://localhost:8000${endpoint}`, {
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
        console.log('Operation successful:', responseData);
        
        // Store the token (if needed)
        localStorage.setItem('access_token', responseData.access_token);

        router.push('/dashboard/candidate');
    } catch (err: any) {
        console.error('Error during form submission:', err);
        setError(err.message);
    }
};



  const toggleForm = () => {
    setIsRegistering(!isRegistering);
    reset();
    setError(null);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-blue-500 to-purple-600">
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
      <div className="flex flex-col min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('/edu.jpg')",  backgroundSize:"85%", backgroundRepeat:"no-repeat", backgroundColor:"white"}}>
      <main className="flex-grow flex items-center justify-center">
        <div className="w-full max-w-md p-8 bg-white bg-opacity-90 rounded-lg shadow-lg relative overflow-hidden">
          <div
            className="absolute top-0 left-0 w-full h-full bg-gray-200 transform transition-transform duration-500 ease-in-out"
            style={{ transform: isRegistering ? 'translateX(-100%)' : 'translateX(0)' }}
          ></div>
          <div className="relative z-10">
            <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
              {isRegistering ? 'Register' : 'Login'}
            </h2>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {isRegistering && (
                <div className="form-group floating-label-group">
                  <input
                    {...register('username')}
                    id="username"
                    name="username"
                    type="text"
                    autoComplete="username"
                    className="input-field"
                    placeholder=" "
                  />
                  <label htmlFor="username" className="floating-label">
                    Username
                  </label>
                  {errors.username && <p className="text-red-500 text-sm mt-1">{errors.username?.message}</p>}
                </div>
              )}

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
                {isRegistering ? 'Register' : 'Login'}
              </button>

              <p className="text-center text-gray-700 mt-4">
                {isRegistering ? 'Already have an account?' : 'Don’t have an account?'}{' '}
                <button
                  type="button"
                  onClick={toggleForm}
                  className="text-blue-500 font-semibold"
                >
                  {isRegistering ? 'Login' : 'Register'}
                </button>
              </p>

              <Link href="/password-recovery" className="text-blue-500 text-center block mt-4">
                Forgot Password?
              </Link>
            </form>
          </div>
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
          background-color: white;
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
    </div>
  );
}
