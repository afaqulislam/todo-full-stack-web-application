import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export function middleware(request: NextRequest) {
  // Get the access token cookie
  const accessToken = request.cookies.get('access_token')?.value;

  // Define protected routes
  const protectedPaths = ['/dashboard', '/dashboard/*', '/api/v1/todos*', '/api/v1/auth/me'];

  // Check if the current path is protected
  const isProtectedPath = protectedPaths.some(path => {
    if (path.endsWith('*')) {
      return request.nextUrl.pathname.startsWith(path.slice(0, -1));
    }
    return request.nextUrl.pathname === path;
  });

  // If accessing a protected route without a token, redirect to login
  if (isProtectedPath && !accessToken) {
    // For API requests, return a 401 response instead of redirecting
    if (request.nextUrl.pathname.startsWith('/api/')) {
      return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }

    // For page requests, redirect to login
    const url = request.nextUrl.clone();
    url.pathname = '/auth/login';
    url.search = `?callback=${encodeURIComponent(request.nextUrl.pathname)}`;
    return NextResponse.redirect(url);
  }

  // Continue with the request if authenticated
  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
    '/dashboard/:path*',
    '/api/v1/todos/:path*',
    '/api/v1/auth/me',
  ],
};