#!/usr/bin/env python3
"""
Advanced Python: Asyncio Patterns

This tutorial covers advanced asyncio patterns including:
- Semaphores for rate limiting
- Event and Condition for coordination
- Locks for shared resource protection
- Timeouts and retries
- Task groups and structured concurrency (Python 3.11+)

Key Concepts:
- Concurrency control patterns
- Resource management
- Error recovery patterns
- Structured concurrency
"""

import asyncio
import time
import random
from typing import List, Optional
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# PART 1: SEMAPHORES FOR RATE LIMITING
# ============================================================================

class RateLimitedAPI:
    """Simulate an API with rate limiting using semaphores."""
    
    def __init__(self, max_concurrent: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.request_count = 0
    
    async def call_api(self, request_id: int) -> str:
        """
        Make an API call with rate limiting.
        
        The semaphore ensures only max_concurrent calls can run simultaneously.
        """
        async with self.semaphore:
            self.request_count += 1
            current = self.request_count
            
            logger.info(f"Request {request_id} starting (concurrent: {self.semaphore._value})")
            
            # Simulate API call
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            result = f"API response for request {request_id} (total calls: {current})"
            logger.info(f"Request {request_id} completed")
            
            return result


async def run_semaphore_example() -> None:
    """Demonstrate rate limiting with semaphores."""
    print("\n" + "="*60)
    print("PART 1: SEMAPHORES FOR RATE LIMITING")
    print("="*60)
    
    api = RateLimitedAPI(max_concurrent=3)
    
    # Make 10 API calls concurrently
    print("\nMaking 10 API calls with max 3 concurrent:")
    tasks = [api.call_api(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    print(f"\nCompleted {len(results)} API calls")
    print("First 3 results:")
    for result in results[:3]:
        print(f"  - {result}")


# ============================================================================
# PART 2: LOCKS FOR SHARED RESOURCES
# ============================================================================

class BankAccount:
    """Simulate a bank account with async locks for thread safety."""
    
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.lock = asyncio.Lock()
        self.transaction_log: List[str] = []
    
    async def deposit(self, amount: float, customer: str) -> float:
        """Deposit money with lock protection."""
        async with self.lock:
            # Simulate some processing time
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            old_balance = self.balance
            self.balance += amount
            
            log_entry = f"{customer} deposited ${amount:.2f}, balance: ${old_balance:.2f} → ${self.balance:.2f}"
            self.transaction_log.append(log_entry)
            
            logger.info(log_entry)
            return self.balance
    
    async def withdraw(self, amount: float, customer: str) -> Optional[float]:
        """Withdraw money with lock protection and balance check."""
        async with self.lock:
            # Simulate some processing time
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            if self.balance >= amount:
                old_balance = self.balance
                self.balance -= amount
                
                log_entry = f"{customer} withdrew ${amount:.2f}, balance: ${old_balance:.2f} → ${self.balance:.2f}"
                self.transaction_log.append(log_entry)
                
                logger.info(log_entry)
                return self.balance
            else:
                log_entry = f"{customer} failed to withdraw ${amount:.2f}, insufficient funds (balance: ${self.balance:.2f})"
                self.transaction_log.append(log_entry)
                
                logger.warning(log_entry)
                return None
    
    async def get_balance(self) -> float:
        """Get current balance with lock protection."""
        async with self.lock:
            await asyncio.sleep(0.05)  # Simulate read delay
            return self.balance


async def run_lock_example() -> None:
    """Demonstrate locks for shared resource protection."""
    print("\n" + "="*60)
    print("PART 2: LOCKS FOR SHARED RESOURCES")
    print("="*60)
    
    account = BankAccount(initial_balance=1000.0)
    
    # Simulate multiple customers accessing the account concurrently
    print("\nSimulating concurrent bank transactions:")
    
    transactions = [
        account.deposit(200.0, "Alice"),
        account.withdraw(150.0, "Bob"),
        account.deposit(300.0, "Charlie"),
        account.withdraw(500.0, "David"),
        account.withdraw(1000.0, "Eve"),  # Should fail
        account.get_balance(),
        account.deposit(50.0, "Frank"),
    ]
    
    results = await asyncio.gather(*transactions)
    
    final_balance = await account.get_balance()
    print(f"\nFinal balance: ${final_balance:.2f}")
    
    print("\nTransaction log:")
    for i, entry in enumerate(account.transaction_log[-5:], 1):
        print(f"  {i}. {entry}")


# ============================================================================
# PART 3: EVENTS AND CONDITIONS FOR COORDINATION
# ============================================================================

class DownloadManager:
    """Manage concurrent downloads with coordination events."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.ready_event = asyncio.Event()
        self.complete_event = asyncio.Event()
        self.downloaded_files: List[str] = []
        self.lock = asyncio.Lock()
    
    async def download_worker(self, worker_id: int) -> None:
        """Worker that waits for ready signal, then downloads files."""
        print(f"  Worker {worker_id} waiting for ready signal...")
        await self.ready_event.wait()
        
        # Simulate downloading 2 files
        for i in range(2):
            file_id = worker_id * 10 + i
            await asyncio.sleep(random.uniform(0.3, 0.7))
            
            async with self.lock:
                self.downloaded_files.append(f"file_{file_id}.txt")
            
            logger.info(f"Worker {worker_id} downloaded file_{file_id}.txt")
        
        # Check if all workers are done
        async with self.lock:
            if len(self.downloaded_files) >= self.max_workers * 2:
                self.complete_event.set()
                print(f"  Worker {worker_id} triggered completion!")
    
    async def start_downloads(self) -> List[str]:
        """Start the download process and wait for completion."""
        print(f"\nStarting download manager with {self.max_workers} workers...")
        
        # Create worker tasks
        workers = [
            asyncio.create_task(self.download_worker(i))
            for i in range(self.max_workers)
        ]
        
        # Wait a moment, then signal workers to start
        await asyncio.sleep(1.0)
        print("\nSignaling workers to start downloads...")
        self.ready_event.set()
        
        # Wait for completion
        print("Waiting for all downloads to complete...")
        await self.complete_event.wait()
        
        # Cancel any remaining worker tasks
        for worker in workers:
            worker.cancel()
        
        await asyncio.gather(*workers, return_exceptions=True)
        
        return self.downloaded_files


async def run_event_example() -> None:
    """Demonstrate events for task coordination."""
    print("\n" + "="*60)
    print("PART 3: EVENTS AND CONDITIONS FOR COORDINATION")
    print("="*60)
    
    manager = DownloadManager(max_workers=3)
    downloaded = await manager.start_downloads()
    
    print(f"\nDownloaded {len(downloaded)} files:")
    for file in downloaded:
        print(f"  - {file}")


# ============================================================================
# PART 4: TIMEOUTS AND RETRIES
# ============================================================================

class UnreliableService:
    """Simulate an unreliable service that sometimes fails or times out."""
    
    def __init__(self, failure_rate: float = 0.3):
        self.failure_rate = failure_rate
        self.call_count = 0
    
    async def call_with_retries(self, 
                               operation: str, 
                               max_retries: int = 3,
                               timeout: float = 2.0) -> str:
        """
        Call an unreliable service with retries and timeout.
        
        Demonstrates:
        1. Timeout handling with asyncio.wait_for
        2. Exponential backoff for retries
        3. Circuit breaker pattern (simplified)
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            self.call_count += 1
            
            try:
                # Try the operation with timeout
                result = await asyncio.wait_for(
                    self._unreliable_operation(operation, attempt),
                    timeout=timeout
                )
                
                if attempt > 0:
                    logger.info(f"Operation '{operation}' succeeded on attempt {attempt + 1}")
                
                return result
                
            except asyncio.TimeoutError:
                last_error = f"Timeout after {timeout} seconds"
                logger.warning(f"Attempt {attempt + 1} for '{operation}': {last_error}")
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} for '{operation}': {last_error}")
            
            # Exponential backoff before retry
            if attempt < max_retries:
                backoff = 0.5 * (2 ** attempt)  # 0.5, 1.0, 2.0 seconds
                logger.info(f"  Waiting {backoff:.1f}s before retry...")
                await asyncio.sleep(backoff)
        
        # All retries failed
        raise Exception(f"Operation '{operation}' failed after {max_retries + 1} attempts. Last error: {last_error}")
    
    async def _unreliable_operation(self, operation: str, attempt: int) -> str:
        """Simulate an unreliable operation that may fail or hang."""
        # Simulate random failure
        if random.random() < self.failure_rate:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            raise Exception(f"Random failure for {operation}")
        
        # Simulate occasional timeout (hanging)
        if random.random() < 0.2:
            hang_time = 3.0  # Longer than our timeout
            await asyncio.sleep(hang_time)
        
        # Normal operation
        processing_time = random.uniform(0.3, 1.0)
        await asyncio.sleep(processing_time)
        
        return f"Success: {operation} completed in {processing_time:.2f}s (attempt {attempt + 1})"


async def run_timeout_retry_example() -> None:
    """Demonstrate timeout and retry patterns."""
    print("\n" + "="*60)
    print("PART 4: TIMEOUTS AND RETRIES")
    print("="*60)
    
    service = UnreliableService(failure_rate=0.4)
    
    print("\nTesting unreliable service with retries and timeout:")
    
    operations = [
        "fetch_user_data",
        "process_payment",
        "update_inventory",
        "send_notification"
    ]
    
    tasks = [
        service.call_with_retries(op, max_retries=2, timeout=1.5)
        for op in operations
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    print(f"\nService was called {service.call_count} times")
    print("\nResults:")
    for op, result in zip(operations, results):
        if isinstance(result, Exception):
            print(f"  {op}: FAILED - {result}")
        else:
            print(f"  {op}: {result}")


# ============================================================================
# PART 5: TASK GROUPS (PYTHON 3.11+)
# ============================================================================

async def run_task_group_example() -> None:
    """Demonstrate structured concurrency with task groups (Python 3.11+)."""
    print("\n" + "="*60)
    print("PART 5: TASK GROUPS (STRUCTURED CONCURRENCY)")
    print("="*60)
    
    try:
        # Try to use the new task group syntax
        async with asyncio.TaskGroup() as tg:
            print("\nCreating tasks in a task group...")
            
            # Create multiple tasks
            task1 = tg.create_task(asyncio.sleep(0.5), name="task1")
            task2 = tg.create_task(asyncio.sleep(0.3), name="task2")
            task3 = tg.create_task(asyncio.sleep(0.7), name="task3")
            
            print("All tasks created, waiting for completion...")
        
        print("Task group completed successfully!")
        
    except AttributeError:
        print("\nNote: Task groups require Python 3.11+")
        print("Falling back to asyncio.gather for demonstration...")
        
        # Fallback for older Python versions
        async def mock_task(name: str, delay: float) -> str:
            await asyncio.sleep(delay)
            return f"{name} completed"
        
        tasks = [
            mock_task("task1", 0.5),
            mock_task("task2", 0.3),
            mock_task("task3", 0.7)
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"Tasks completed: {results}")


# ============================================================================
# PART 6: QUEUES FOR WORK DISTRIBUTION
# ============================================================================

@dataclass
class WorkItem:
    """Represents a unit of work to be processed."""
    id: int
    data: str
    priority: int = 1  # Lower number = higher priority


class PriorityWorkerPool:
    """A worker pool that processes items from a priority queue."""
    
    def __init__(self, num_workers: int = 3):
        self.num_workers = num_workers
        # Use a priority queue (lower priority number = higher priority)
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.workers: List[asyncio.Task] = []
        self.processed_items: List[WorkItem] = []
    
    async def worker(self, worker_id: int) -> None:
        """Worker that processes items from the queue."""
        while True:
            try:
                # Get item from queue (priority, work_item)
                priority, work_item = await self.queue.get()
                
                logger.info(f"Worker {worker_id} processing {work_item.data} (priority: {priority})")
                
                # Simulate processing time
                await asyncio.sleep(random.uniform(0.2, 0.8))
                
                # Mark item as processed
                self.processed_items.append(work_item)
                self.queue.task_done()
                
                logger.info(f"Worker {worker_id} completed {work_item.data}")
                
            except asyncio.CancelledError:
                logger.info(f"Worker {worker_id} shutting down")
                break
    
    async def add_work(self, work_item: WorkItem) -> None:
        """Add a work item to the queue."""
        await self.queue.put((work_item.priority, work_item))
    
    async def run(self, work_items: List[WorkItem]) -> List[WorkItem]:
        """Run the worker pool with given work items."""
        print(f"\nStarting worker pool with {self.num_workers} workers...")
        
        # Start workers
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]
        
        # Add all work items
        for item in work_items:
            await self.add_work(item)
        
        # Wait for all items to be processed
        await self.queue.join()
        
        # Stop workers
        for worker in self.workers:
            worker.cancel()
        
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        return self.processed_items


async def run_queue_example() -> None:
    """Demonstrate priority queues for work distribution."""
    print("\n" + "="*60)
    print("PART 6: PRIORITY QUEUES FOR WORK DISTRIBUTION")
    print("="*60)
    
    # Create work items with different priorities
    work_items = [
        WorkItem(1, "Critical system update", priority=1),
        WorkItem(2, "User report generation", priority=3),
        WorkItem(3, "Emergency alert", priority=1),
        WorkItem(4, "Daily backup", priority=4),
        WorkItem(5, "Data sync", priority=2),
        WorkItem(6, "Log cleanup", priority=5),
        WorkItem(7, "Security scan", priority=2),
        WorkItem(8, "Performance metrics", priority=3),
    ]
    
    pool = PriorityWorkerPool(num_workers=2)
    processed = await pool.run(work_items)
    
    print(f"\nProcessed {len(processed)} items:")
    for item in processed:
        print(f"  - [{item.priority}] {item.data}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main() -> None:
    """Run all asyncio pattern examples."""
    print("="*60)
    print("ADVANCED PYTHON: ASYNCIO PATTERNS TUTORIAL")
    print("="*60)
    
    try:
        await run_semaphore_example()
        await run_lock_example()
        await run_event_example()
        await run_timeout_retry_example()
        await run_task_group_example()
        await run_queue_example()
        
        print("\n" + "="*60)
        print("TUTORIAL COMPLETE!")
        print("="*60)
        print("\nKey Patterns Covered:")
        print("1. Semaphores - Rate limiting and resource pooling")
        print("2. Locks - Protecting shared resources")
        print("3. Events - Coordinating task execution")
        print("4. Timeouts & Retries - Handling unreliable operations")
        print("5. Task Groups - Structured concurrency (Python 3.11+)")
        print("6. Priority Queues - Work distribution with priorities")
        
    except Exception as e:
        logger.error(f"Error in tutorial: {e}")
        raise


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())