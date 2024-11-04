/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';

const nextConfig = {
  output: 'export',
  assetPrefix: isProd ? '/<your-repo-name>/' : '',
  basePath: isProd ? '/<your-repo-name>' : '',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

