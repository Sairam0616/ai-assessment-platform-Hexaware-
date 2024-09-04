"use client";

import React, { useState } from 'react';
import Link from 'next/link';

// Define type for CSS properties
interface CSSProperties {
  [key: string]: React.CSSProperties[keyof React.CSSProperties];
}

const Home: React.FC = () => {
  const [activeCard, setActiveCard] = useState<string | null>(null);

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gray-900 overflow-hidden text-white">
      <div style={styles.background}></div>
      <div style={styles.overlay}></div>
      <h1 style={styles.heading}>Welcome to the AI-Assessment Platform</h1>
      <p style={styles.subheading}>Please select your role to continue:</p>
      <div style={styles.cardContainer}>
        <Card
          title="Candidate"
          description="Participate in assessments to showcase your skills."
          link="/login/candidate"
          isActive={activeCard === 'candidate'}
          onMouseEnter={() => setActiveCard('candidate')}
          onMouseLeave={() => setActiveCard(null)}
        />
        <Card
          title="Educator/Instructor"
          description="Design and create assessments tailored to specific skills."
          link="/login/educator"
          isActive={activeCard === 'educator'}
          onMouseEnter={() => setActiveCard('educator')}
          onMouseLeave={() => setActiveCard(null)}
        />
        <Card
          title="Administrator"
          description="Manage the assessment process and ensure smooth operation."
          link="/login/admin"
          isActive={activeCard === 'admin'}
          onMouseEnter={() => setActiveCard('admin')}
          onMouseLeave={() => setActiveCard(null)}
        />
      </div>
      <style jsx>{`
        .background {
          position: absolute;
          inset: 0;
          background: url('public/ai_img.jpg');
          background-size: cover;
          z-index: -3; /* Ensure background is behind content */
        }

        @keyframes gradientShift {
          0% {
            background-position: 0% 0%;
          }
          50% {
            background-position: 100% 100%;
          }
          100% {
            background-position: 0% 0%;
          }
        }

        @keyframes float {
          0% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
          100% {
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

interface CardProps {
  title: string;
  description: string;
  link: string;
  isActive: boolean;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
}

const Card: React.FC<CardProps> = ({ title, description, link, isActive, onMouseEnter, onMouseLeave }) => (
  <Link href={link} passHref>
    <div
      style={{
        ...styles.card,
        ...(isActive ? styles.cardActive : styles.cardInactive),
      }}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div style={styles.cardContent}>
        <h2 style={styles.cardTitle}>{title}</h2>
        <p style={styles.cardDescription}>{description}</p>
      </div>
    </div>
  </Link>
);

const styles: { [key: string]: CSSProperties } = {
  heading: {
    fontSize: '3rem',
    fontWeight: 'bold',
    marginBottom: '1.5rem',
    zIndex: 10,
    textAlign: 'center',
  },
  subheading: {
    fontSize: '1.5rem',
    marginBottom: '2rem',
    zIndex: 10,
    textAlign: 'center',
  },
  cardContainer: {
    display: 'flex',
    gap: '1.5rem',
    zIndex: 10,
    position: 'relative',
  },
  card: {
    position: 'relative',
    width: '18rem',
    height: '12rem',
    padding: '1.5rem',
    backgroundColor: 'white',
    borderRadius: '0.75rem',
    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)',
    transform: 'scale(1)',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
    cursor: 'pointer',
    zIndex: 1,
    overflow: 'hidden',
  },
  cardActive: {
    transform: 'scale(1.1)',
    boxShadow: '0 12px 24px rgba(0, 0, 0, 0.3)',
    zIndex: 20,
  },
  cardInactive: {
    opacity: 0.3,
  },
  cardContent: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    color: 'black',
    textAlign: 'center',
  },
  cardTitle: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
  },
  cardDescription: {
    color: '#4a4a4a',
    marginTop: '0.5rem',
  },
};

export default Home;


