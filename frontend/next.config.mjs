/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';

const nextConfig = {
  output: 'export',
  assetPrefix: isProd ? '/<https://github.com/Sairam0616/ai-assessment-platform-Hexaware-/frontend/app/home/page.html>/' : '',
  basePath: isProd ? '/<https://github.com/Sairam0616/ai-assessment-platform-Hexaware-/frontend/app/home/page.html>' : '',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

