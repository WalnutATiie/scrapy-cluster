# Redis host information
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Kafka server information
KAFKA_HOSTS = '127.0.0.1:9092'
KAFKA_INCOMING_TOPIC = 'demo.inbound_actions'
KAFKA_GROUP = 'demo-group'

SCHEMA = "action_schema.json"
SCHEMA_METHOD = "handle_action_request"
