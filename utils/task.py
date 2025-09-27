import asyncio
from asyncio import Task
from utils import logs

logging = logs.get_logger()


# 全局任务集合，用于跟踪和管理所有正在运行的异步任务
class TaskManager:
    def __init__(self):
        self.tasks = set()
        self.tagged_tasks: dict[str, Task] = {}
    
    def add(self, task: asyncio.Task, tag: str = "") -> Task:
        """
        添加任务到全局集合，并可选地为任务添加标签
        
        Args:
            task (asyncio.Task): 要添加的异步任务
            tag (str, optional): 任务标签，默认为空字符串
            
        Returns:
            Task: 添加的异步任务实例
        """
        self.tasks.add(task)
        self.tagged_tasks[tag] = task
        
        return task

    def get_tasks(self, tag: str) -> Task | None:
        """
        根据标签获取任务

        Args:
            tag (str): 任务标签

        Returns:
            Task | None: 对应标签的任务，如果不存在则返回None
        """
        current_task = self.tagged_tasks.get(tag, None)
        if current_task and current_task.done():
            # 如果任务已完成，从集合中移除
            self.remove(current_task)
            return None
        return current_task

    def remove(self, tag: str | Task) -> bool:
        """
        从全局集合中移除任务
        
        Args:
            tag (str | Task): 任务标签或任务实例

        Returns:
            bool: 是否成功移除任务
        """
        task = tag if isinstance(tag, Task) else self.get_tasks(tag)
        if task and task in self.tasks:
            self.tasks.remove(task)
            for k, v in list(self.tagged_tasks.items()):
                if v == task:
                    del self.tagged_tasks[k]
                    break
            return True
        return False
    
    def cancel_all(self):
        """
        取消并清理所有正在运行的异步任务
        
        该函数遍历全局tasks集合中的所有异步任务,
        对每个任务执行取消操作并标记为完成。
        主要用于在开始新对话或应用关闭时确保没有遗留的任务继续运行。
        """
        logging.info("Cancelling all tasks...")
        task: asyncio.Task
        for task in self.tasks:
            if not task.done():
                task.cancel()
        self.tasks.clear()
        self.tagged_tasks.clear()
    
    def clear(self):
        """
        清理已完成或取消的任务
        
        该函数遍历全局tasks集合，移除所有已完成或已取消的任务。
        主要用于定期清理任务集合，防止内存泄漏。
        """
        logging.info("Clearing completed tasks...")
        self.tasks = {task for task in self.tasks if not task.done()}
        self.tagged_tasks = {k: v for k, v in self.tagged_tasks.items() if v in self.tasks}
        
    def is_task(self, tag: str) -> bool:
        """
        检查是否存在指定标签的任务
        
        Args:
            tag (str): 任务标签
            
        Returns:
            bool: 如果存在对应标签的任务且任务未完成，返回True；否则返回False
        """
        task = self.tagged_tasks.get(tag, None)
        return task is not None and not task.done()
    