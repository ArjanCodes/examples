import subprocess
import threading
import time

import redis

type RedisProcess = subprocess.Popen[bytes]

# Flag to control the listener thread
stop_listening = threading.Event()


# Start Redis server locally (this will run as a subprocess)
def start_redis_server() -> RedisProcess:
    process = subprocess.Popen(
        ["redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(0.5)  # Give Redis server a second to start up
    return process


# Stop the Redis server
def stop_redis_server(process: RedisProcess) -> None:
    process.terminate()
    process.wait()


def real_time_data(r: redis.Redis) -> None:
    r.set("page_views", 0)
    r.incr("page_views")
    r.incr("page_views")
    page_views = r.get("page_views").decode("utf-8")
    print(f"Page views: {page_views}")


def task_queue(r: redis.Redis) -> None:
    r.rpush("task_queue", "task1")
    r.rpush("task_queue", "task2")
    r.rpush("task_queue", "task3")

    task = r.lpop("task_queue").decode("utf-8")
    print(f"Processing task: {task}")


def redis_set(r: redis.Redis) -> None:
    r.sadd("unique_users", "user1")
    r.sadd("unique_users", "user2")
    r.sadd("unique_users", "user1")  # Duplicate, will not be added

    unique_users = r.smembers("unique_users")
    print(f"Unique users: {[user.decode('utf-8') for user in unique_users]}")


def expiring_data(r: redis.Redis) -> None:
    r.set("session_token", "abc123", ex=3600)  # Expires in 1 hour
    session_token = r.get("session_token").decode("utf-8")
    print(f"Session token: {session_token} (will expire in 1 hour)")


def pub_sub_messaging(r: redis.Redis) -> None:
    def message_handler(message):
        print(f"Received message: {message['data'].decode('utf-8')}")

    def listen_for_messages():
        p = r.pubsub()
        p.subscribe("my-channel")
        # Listen for messages with a timeout to periodically check for stop signal
        while not stop_listening.is_set():
            message = p.get_message(timeout=1.0)  # Timeout set to 1 second
            if message and message["type"] == "message":
                message_handler(message)

    # Start a thread to listen for messages
    listener_thread = threading.Thread(target=listen_for_messages)
    listener_thread.start()

    # Give the listener a moment to start up
    time.sleep(0.5)

    # Simulate sending a message to the channel
    r.publish("my-channel", "Hello, Redis!")

    # Allow some time for the message to be processed
    time.sleep(0.5)

    # Signal the listener thread to stop
    stop_listening.set()
    listener_thread.join()  # Wait for the listener thread to finish


def main() -> None:
    # Start the Redis server
    redis_process = start_redis_server()

    # Connect to the locally started Redis server
    r = redis.Redis(host="localhost", port=6379, db=0)

    # Example 1: Real-Time Data - Using Redis as a Counter
    real_time_data(r)

    # Example 2: Using Redis Lists for Real-Time Task Queues
    task_queue(r)

    # Example 3: Using Redis Sets to Track Unique Items
    redis_set(r)

    # Example 4: Handling Expiring Data
    expiring_data(r)

    # Example 5: Pub/Sub Messaging with Redis
    pub_sub_messaging(r)

    # Stop the Redis server
    stop_redis_server(redis_process)
    print("Redis server stopped.")


if __name__ == "__main__":
    main()
