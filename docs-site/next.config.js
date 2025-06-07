/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  assetPrefix: process.env.NODE_ENV === 'production' ? '/multiverse-character-generator' : '',
  basePath: process.env.NODE_ENV === 'production' ? '/multiverse-character-generator' : '',
}

module.exports = nextConfig