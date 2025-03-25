import asyncio
import threading
from datetime import datetime
from typing import Callable, Dict, Any
import pytz
from src.utils.logging_config import setup_logger


logger = setup_logger(__name__)


class AsyncJobScheduler:
    def __init__(self):
        self.jobs_dict: Dict[str, Dict[str, Any]] = {}
        self.loop = asyncio.new_event_loop()
        self.scheduler_thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self.scheduler_thread.start()

    def _start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def add_job(self, job_id: str, run_at: datetime, function: Callable, *args, **kwargs):
        """Add a job to the scheduler."""
        if job_id in self.jobs_dict:
            logger.error(f"Job ID '{job_id}' already exists.")

        # Calculate delay until execution
        delay = (run_at - datetime.now(pytz.utc)).total_seconds()
        logger.info(f"Scheduling job '{job_id}' to run at {run_at} UTC ({delay} seconds from now)")
        if delay < 0:
            logger.error("run_at must be a future datetime.")

        # Job metadata
        self.jobs_dict[job_id] = {
            "run_at": run_at,
            "function": function,
            "args": args,
            "kwargs": kwargs,
            "task": None
        }

        # Schedule job in the event loop
        self._schedule_job(job_id, delay)

    def _schedule_job(self, job_id: str, delay: float):
        """Schedule a job to run after a delay."""
        async def delayed_job():
            await asyncio.sleep(delay)
            await self._run_job(job_id)

        task = asyncio.create_task(delayed_job())  # Use create_task here
        self.jobs_dict[job_id]["task"] = task

    async def _run_job(self, job_id: str):
        """Run the job and remove it from the scheduler."""
        try:
            job = self.jobs_dict[job_id]
            logger.info(f"Running job '{job_id}'")
            # Use asyncio.run to ensure the async function is run within the loop
            if asyncio.iscoroutinefunction(job["function"]):
                await job["function"](*job["args"], **job["kwargs"])
            else:
                job["function"](*job["args"], **job["kwargs"])
        except Exception as e:
            logger.error(f"Error running job '{job_id}': {e}")
        finally:
            self.jobs_dict.pop(job_id, None)

    def remove_job(self, job_id: str):
        """Remove a job from the scheduler."""
        if job_id in self.jobs_dict:
            task = self.jobs_dict[job_id]["task"]
            if task is not None:
                task.cancel()
            del self.jobs_dict[job_id]
        else:
            logger.error(f"Job ID '{job_id}' does not exist.")

    def update_job_time(self, job_id: str, new_run_at: datetime):
        """Update the scheduled time for an existing job."""
        if job_id not in self.jobs_dict:
            logger.error(f"Job ID '{job_id}' does not exist.")

        # Calculate new delay
        delay = (new_run_at - datetime.now(pytz.utc)).total_seconds()
        if delay < 0:
            logger.error("new_run_at must be a future datetime.")
            return

        # Cancel existing task
        task = self.jobs_dict[job_id]["task"]
        if task is not None:
            task.cancel()

        self.jobs_dict[job_id]["run_at"] = new_run_at

        # Re-Schedule job
        self._schedule_job(job_id, delay)

    def get_jobs(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of scheduled jobs."""
        return self.jobs_dict
