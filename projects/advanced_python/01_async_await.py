#!/usr/bin/env python3
"""
Advanced Python: Async/Await Fundamentals

This tutorial covers Python's async/await syntax, coroutines, and event loops.
Learn how to write concurrent code that can handle I/O-bound operations efficiently.

Key Concepts:
- Coroutines and async/await syntax
- Event loops and task scheduling
- Concurrent vs parallel execution
- I/O-bound vs CPU-bound operations
"""

import asyncio
import time
import aiohttp
from typing import List, Coroutine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# PART 1: BASIC ASYNC/AWAIT
# ============================================================================

async def simple_coroutine(name: str, delay: float) -> str:
    """
    A simple coroutine that sleeps for a given delay.
    
    Args:
        name: Identifier for this coroutine
        delay: Time to sleep in seconds
        
    Returns:
        A message indicating completion
    """
    logger.info(f"Coroutine '{name}' starting, will sleep for {delay} seconds")
    await asyncio.sleep(delay)
    logger.info(f"Coroutine '{name}' finished after {delay} seconds")
    return f"Coroutine '{name}' completed"


async def run_basic_example() -> None:
    """Demonstrate basic async/await with multiple coroutines."""
    print("\n" + "="*60)
    print("PART 1: BASIC ASYNC/AWAIT")
    print("="*60)
    
    # Run coroutines sequentially (not concurrent)
    print("\n1. Running coroutines sequentially:")
    start = time.time()
    
    result1 = await simple_coroutine("Task1", 1.0)
    result2 = await simple_coroutine("Task2", 0.5)
    
    elapsed = time.time() - start
    print(f"   Sequential execution took {elapsed:.2f} seconds")
    print(f"   Results: {result1}, {result2}")
    
    # Run coroutines concurrently using asyncio.gather
    print("\n2. Running coroutines concurrently with asyncio.gather:")
    start = time.time()
    
    results = await asyncio.gather(
        simple_coroutine("TaskA", 1.0),
        simple_coroutine("TaskB", 0.5),
        simple_coroutine("TaskC", 0.8)
    )
    
    elapsed = time.time() - start
    print(f"   Concurrent execution took {elapsed:.2f} seconds")
    print(f"   Results: {results}")
    
    # Demonstrate that the longest task determines total time
    print("\n3. Demonstrating concurrency (not parallelism):")
    print("   Note: Total time ≈ max(delay1, delay2, delay3), not sum(delays)")


# ============================================================================
# PART 2: EVENT LOOPS AND TASKS
# ============================================================================

async def cpu_intensive_task(n: int) -> int:
    """
    Simulate a CPU-intensive task (Fibonacci calculation).
    
    Note: This is CPU-bound, not I/O-bound, so async won't help much.
    Use asyncio.to_thread() or multiprocessing for CPU-bound tasks.
    """
    def fib(x: int) -> int:
        if x <= 1:
            return x
        return fib(x - 1) + fib(x - 2)
    
    # Run in a thread to avoid blocking the event loop
    return await asyncio.to_thread(fib, n)


async def io_bound_task(url: str) -> tuple[str, int]:
    """
    Simulate an I/O-bound task (HTTP request).
    
    This is where async truly shines - while waiting for network response,
    other tasks can run.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                return url, response.status
        except Exception as e:
            return url, f"Error: {e}"


async def run_event_loop_example() -> None:
    """Demonstrate event loops, tasks, and different types of operations."""
    print("\n" + "="*60)
    print("PART 2: EVENT LOOPS AND TASKS")
    print("="*60)
    
    # Create tasks explicitly
    print("\n1. Creating and managing tasks:")
    
    # Create task objects (they start running immediately)
    task1 = asyncio.create_task(simple_coroutine("ExplicitTask1", 0.3))
    task2 = asyncio.create_task(simple_coroutine("ExplicitTask2", 0.2))
    
    # Wait for tasks to complete
    await task1
    await task2
    
    print(f"   Task1 result: {task1.result()}")
    print(f"   Task2 result: {task2.result()}")
    
    # Demonstrate I/O-bound tasks
    print("\n2. I/O-bound tasks (HTTP requests):")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404"
    ]
    
    start = time.time()
    http_tasks = [io_bound_task(url) for url in urls]
    http_results = await asyncio.gather(*http_tasks)
    
    elapsed = time.time() - start
    print(f"   Fetched {len(urls)} URLs in {elapsed:.2f} seconds")
    for url, status in http_results:
        print(f"   - {url}: {status}")
    
    # Demonstrate CPU-bound tasks (run in threads)
    print("\n3. CPU-bound tasks (run in threads to avoid blocking):")
    
    start = time.time()
    cpu_tasks = [cpu_intensive_task(n) for n in [30, 31, 32]]
    cpu_results = await asyncio.gather(*cpu_tasks)
    
    elapsed = time.time() - start
    print(f"   Calculated 3 Fibonacci numbers in {elapsed:.2f} seconds")
    for n, result in zip([30, 31, 32], cpu_results):
        print(f"   - fib({n}) = {result}")


# ============================================================================
# PART 3: ADVANCED PATTERNS
# ============================================================================

async def producer(queue: asyncio.Queue, item_count: int) -> None:
    """Produce items and put them in the queue."""
    for i in range(item_count):
        await queue.put(f"Item-{i}")
        await asyncio.sleep(0.1)  # Simulate work
        logger.info(f"Produced Item-{i}")
    
    # Signal completion
    await queue.put(None)


async def consumer(queue: asyncio.Queue, consumer_id: int) -> None:
    """Consume items from the queue."""
    while True:
        item = await queue.get()
        
        if item is None:
            # Put the signal back for other consumers
            await queue.put(None)
            break
        
        logger.info(f"Consumer-{consumer_id} processing {item}")
        await asyncio.sleep(0.2)  # Simulate processing time
        queue.task_done()


async def run_producer_consumer_pattern() -> None:
    """Demonstrate producer-consumer pattern with asyncio.Queue."""
    print("\n" + "="*60)
    print("PART 3: PRODUCER-CONSUMER PATTERN")
    print("="*60)
    
    queue = asyncio.Queue(maxsize=5)
    item_count = 10
    
    # Create producer and consumers
    producer_task = asyncio.create_task(producer(queue, item_count))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)  # 3 consumers
    ]
    
    # Wait for producer to finish
    await producer_task
    
    # Wait for all items to be processed
    await queue.join()
    
    # Cancel consumers (they'll exit when they see None)
    for task in consumer_tasks:
        task.cancel()
    
    # Wait for consumers to finish
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
    
    print(f"\n   Produced {item_count} items with 3 consumers")
    print("   Pattern complete!")


# ============================================================================
# PART 4: ERROR HANDLING AND CANCELLATION
# ============================================================================

async def task_with_error(task_id: int) -> str:
    """A task that might raise an error."""
    await asyncio.sleep(0.5)
    
    if task_id % 3 == 0:
        raise ValueError(f"Task {task_id} failed intentionally")
    
    return f"Task {task_id} succeeded"


async def run_error_handling_example() -> None:
    """Demonstrate error handling in async code."""
    print("\n" + "="*60)
    print("PART 4: ERROR HANDLING AND CANCELLATION")
    print("="*60)
    
    # Using return_exceptions with asyncio.gather
    print("\n1. Error handling with asyncio.gather:")
    
    tasks = [task_with_error(i) for i in range(6)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"   Task {i}: ERROR - {result}")
        else:
            print(f"   Task {i}: SUCCESS - {result}")
    
    # Task cancellation
    print("\n2. Task cancellation:")
    
    async def long_running_task() -> str:
        try:
            await asyncio.sleep(10)  # Simulate long operation
            return "Task completed"
        except asyncio.CancelledError:
            logger.warning("Task was cancelled!")
            raise  # Re-raise to properly cancel
    
    task = asyncio.create_task(long_running_task())
    
    # Cancel after 0.5 seconds
    await asyncio.sleep(0.5)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("   Task was successfully cancelled")
    
    # Timeouts
    print("\n3. Timeouts with asyncio.wait_for:")
    
    async def slow_task() -> str:
        await asyncio.sleep(2)
        return "Slow task completed"
    
    try:
        result = await asyncio.wait_for(slow_task(), timeout=1.0)
        print(f"   Result: {result}")
    except asyncio.TimeoutError:
        print("   Task timed out after 1 second")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main() -> None:
    """Run all examples."""
    print("="*60)
    print("ADVANCED PYTHON: ASYNC/AWAIT TUTORIAL")
    print("="*60)
    
    try:
        await run_basic_example()
        await run_event_loop_example()
        await run_producer_consumer_pattern()
        await run_error_handling_example()
        
        print("\n" + "="*60)
        print("TUTORIAL COMPLETE!")
        print("="*60)
        print("\nKey Takeaways:")
        print("1. Use async/await for I/O-bound operations (network, file I/O)")
        print("2. Use asyncio.gather() to run multiple coroutines concurrently")
        print("3. For CPU-bound tasks, use asyncio.to_thread() or multiprocessing")
        print("4. Always handle errors and timeouts in async code")
        print("5. Use asyncio.Queue for producer-consumer patterns")
        
    except Exception as e:
        logger.error(f"Error in tutorial: {e}")
        raise


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())