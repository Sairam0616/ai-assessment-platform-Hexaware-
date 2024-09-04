// import { NextRequest, NextResponse } from 'next/server';

// interface LoginRequest {
//   email: string;
//   password: string;
// }

// export async function POST(req: NextRequest): Promise<NextResponse> {
//   try {
//     // Parse the request body
//     const { email, password }: LoginRequest = await req.json();

//     // Here you'd normally validate the credentials against a database
//     if (email === 'admin@example.com' && password === 'password') {
//       return NextResponse.json({ success: true }, { status: 200 });
//     } else {
//       return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 });
//     }
//   } catch (error) {
//     console.error('Error handling POST request:', error);
//     return NextResponse.json({ message: 'Internal server error' }, { status: 500 });
//   }
// }
