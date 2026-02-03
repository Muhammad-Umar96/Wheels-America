# Scrapy settings for wheelsamerica project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "wheelsamerica"

SPIDER_MODULES = ["wheelsamerica.spiders"]
NEWSPIDER_MODULE = "wheelsamerica.spiders"

ADDONS = {}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "wheelsamerica (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    "wheelsamerica.middlewares.RotateAgentMiddleware": 543,
}

CONCURRENT_REQUESTS = 8  # Much lower concurrency
DOWNLOAD_DELAY = 1.0     # Wait 1 second between requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Randomize delay (0.5-1.5x)

# Retry settings
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Enable and configure the AutoThrottle extension
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 2
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# HTTP Caching
HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.DummyPolicy'

# Logging
# LOG_LEVEL = 'INFO'
LOG_FILE='spider.log'

# Feed settings
FEED_EXPORT_ENCODING = "utf-8-sig"
