# AI-Assessment Platform 

## Overview

The AI-Assessment Platform is a scalable and secure web application designed to facilitate AI-driven assessments. The platform allows different user roles, such as candidates, educators, and administrators, to interact with a dynamic and user-friendly interface.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Functional Architecture](#functional-architecture)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Architecture

### System Architecture Diagram

![System Architecture Diagram](link_to_system_architecture_diagram.png)

The system architecture of the AI-Assessment Platform includes:

- **Frontend:** Built using Next.js and Tailwind CSS, it handles the user interface, including login/register pages, role-specific dashboards, and assessment interfaces.
- **API Gateway:** Acts as an intermediary between the frontend and backend, managing API requests and routing them to appropriate services.
- **Backend:** Powered by FastAPI, it includes services for authentication, user management, and assessment management.
- **Database:** MongoDB is used for storing user profiles, assessments, and results, while a vector database is employed for advanced similarity searches and recommendations.
- **Security:** The platform uses JWT tokens for secure user authentication and role-based access control.

## Functional Architecture

The functional architecture outlines how the system components interact to deliver a seamless user experience. Users begin by interacting with the frontend, where they can log in, register, and access role-specific dashboards.

## Technology Stack

- **Frontend:** Next.js, Tailwind CSS, TypeScript
- **Backend:** FastAPI, Python, MongoDB, JWT for authentication
- **Vector Database:** Pinecone or Milvus
- **Deployment:** Docker, Uvicorn

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-assessment-platform.git
cd ai-assessment-platform
cd backend
```
### 2. Set Up the Backend
1.Navigate to the backend directory:
```bash
cd backend
```
2.Install dependencies using Poetry:
```bash
poetry install
```
3.Create a .env file and set up environment variables:
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=mongodb://localhost:27017/app_db
```
4.Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
### 3. Set Up the Frontend
1.Navigate to the frontend directory:
```bash
cd ../frontend
```
2.Install dependencies using npm:
```bash
npm install
```
3.Start the Next.js development server:
```bash
npm run dev
```
### 4. Access the Application
Frontend: http://localhost:3000
Backend (API): http://localhost:8000

### API Documentation
The backend API is documented using OpenAPI. You can access the interactive API docs by navigating to http://localhost:8000/docs when the backend server is running.

### Contributing
We welcome contributions to the AI-Assessment Platform. Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a pull request.

