import { NextResponse } from 'next/server';

export async function GET() {
  // Example data fetching (could be from a database)
  const roles = [
    { id: 'candidate', name: 'Candidate' },
    { id: 'educator', name: 'Educator' },
    { id: 'admin', name: 'Administrator' }
  ];

  return NextResponse.json(roles);
}
