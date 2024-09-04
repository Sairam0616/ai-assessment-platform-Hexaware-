import React from 'react';

interface AuthButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
}

const AuthButton: React.FC<AuthButtonProps> = ({ children, type = 'submit', ...props }) => {
  return (
    <button
      type={type}
      className="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md group hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      {...props}
    >
      {children}
    </button>
  );
};

export default AuthButton;

