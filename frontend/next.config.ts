import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'https://afaqulislam-todo-full-stack-web-application-backend.hf.space/api/v1/:path*',
      },
    ];
  },
};

export default nextConfig;
