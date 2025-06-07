/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  assetPrefix: process.env.NODE_ENV === 'production' ? '/character_generator' : '',
  basePath: process.env.NODE_ENV === 'production' ? '/character_generator' : '',
}

module.exports = nextConfig