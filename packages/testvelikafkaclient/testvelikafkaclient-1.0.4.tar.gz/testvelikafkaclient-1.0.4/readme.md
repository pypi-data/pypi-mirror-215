### Kafka Client for VELI.STORE

### Description

This module helps you to integration kafka messaging into your apps.
Supported frameworks: FastAPI, (Django coming soon :D)

### How to use (FastAPI):

* Producer

```python
app = FastAPI()


def produce_event(topic, event):
    producer = app.state.producer
    producer.produce_event(topic, event)


@app.on_event("startup")
async def startup_event():
    bootstrap_servers = ['localhost:9092', 'localhost:9093']
    producer = KafkaEventProducer(bootstrap_servers)
    await producer.start()
    app.state.producer = producer

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.producer.stop()

@app.post("/products")
async def save_product(product_info: ProductInfo):
    product = save_product(product_info)
    produce_event(KafkaTopic.PAGE_VIEWS, product)
    return product
```

* Consumer

```python
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Define the configuration variables
    topics = [KafkaTopic.USER_REGISTRATIONS, KafkaTopic.PAGE_VIEWS]
    bootstrap_servers = ['localhost:9092', 'localhost:9093']
    group_id = 'app_id'

    consumer = AsyncKafkaConsumer(topics, bootstrap_servers, group_id)
    app.state.consumer = consumer
    await consumer.start()
    # start the consume_events coroutine in the background
    asyncio.create_task(consumer.consume())


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.consumer.stop()
```