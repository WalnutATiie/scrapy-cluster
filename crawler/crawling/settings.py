# Specify the host and port to use when connecting to Redis.
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Kafka server information
KAFKA_HOSTS = '52caff821b0f:9092'
KAFKA_TOPIC_PREFIX = 'demo'

# Scrapy Settings
# ~~~~~~~~~~~~~~~

# Scrapy settings for distributed_crawling project
#
BOT_NAME = 'crawling'

SPIDER_MODULES = ['crawling.spiders']
NEWSPIDER_MODULE = 'crawling.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "crawling.distributed_scheduler.DistributedScheduler"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# how long we want the duplicate timeout queues to stick around in seconds
DUPEFILTER_TIMEOUT = 60

# how many times to retry getting an item from the queue before the spider is considered idle
SCHEUDLER_ITEM_RETRIES = 3

# Store scraped item in redis for post-processing.
ITEM_PIPELINES = {
    'crawling.pipelines.KafkaPipeline': 100,
}

SPIDER_MIDDLEWARES = {
    # disable built-in DepthMiddleware, since we do our own
    # depth management per crawl request
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,
}

DOWNLOADER_MIDDLEWARES = {
    # Handle timeout retries with the redis scheduler and logger
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : None,
    'crawling.redis_retry_middleware.RedisRetryMiddleware': 510,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    #'crawling.proxy_middleware.ProxyMiddleware': 760,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 800,
}

# Disable the built in logging in production
LOG_ENABLED = True 
LOG_LEVEL = 'INFO'
# Allow all return codes
HTTPERROR_ALLOW_ALL = True

RETRY_TIMES = 3
#CONCURRENT_REQUESTS = 200
DOWNLOAD_TIMEOUT = 60
PROXIES = [
  {'ip_port': '47.88.3.97:9398', 'user_pass': ''},
  {'ip_port': '47.88.26.105:9398', 'user_pass': ''},
  {'ip_port': '47.88.7.56:9398','user_pass': ''},
  {'ip_port': '47.88.7.62:9398','user_pass': ''},
  {'ip_port': '47.88.6.231:9398','user_pass': ''},
  {'ip_port': '47.88.7.9:9398','user_pass': ''},
  {'ip_port': '47.88.6.172:9398','user_pass': ''},
]
# Local Overrides
# ~~~~~~~~~~~~~~~

try:
    from localsettings import *
except ImportError:
    pass
