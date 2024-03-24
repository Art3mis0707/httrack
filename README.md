# Multimodal Dataset Creation

# Web Crawler and Content Filtering Pipeline

This repository contains a pipeline for crawling HTML, web texts, images, and videos from the Internet while implementing strict filtering mechanisms to ensure safe and appropriate content.

## Features

- **Web Crawling**: Crawl HTML, texts, and links to images and videos from the Internet, initialized with popular website URLs or URLs extracted from Common Crawl.
- **Intelligent Crawling**: Implement rate-limiting and URL bucketing to avoid excessive retrieval from individual servers.
- **Deduplication**: Utilize Bloom filters to prevent crawling and storing duplicate links.
- **Text Certification (Optional)**: Explore techniques for certifying texts using hashes or KenLM perplexity buckets.
- **Image Downloading**: Leverage the img2 dataset for downloading images.
- **Video Downloading**: Utilize the Video2 dataset for downloading videos.
- **Content Filtering**: Employ keyword-based filters, CLIP-based filters (with a quantized version optimized for CPUs), and various linear models that take CLIP vectors as input for NSFW detection, aesthetic scoring, and ImageNet 1k label prediction.
- **Aggressive Filtering**: Implement aggressive filtering thresholds to ensure only safe and appropriate content is included.
- **Centralized Storage**: Option to send crawled and filtered content to a central storage server, assuming a centralized organization operates the workers in a swarm.

