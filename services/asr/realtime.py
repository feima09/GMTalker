from .wake import Wake, logging
import asyncio


class Realtime(Wake):
    async def speech(self) -> str:
        text = ""
        queue = asyncio.Queue()

        async def collect_text():
            self.funasr.status = True
            async for data in self.funasr.receive():
                logging.info(data)
                await queue.put(data)

        try:
            task = asyncio.create_task(collect_text())
            while True:
                if text == "":
                    self.tasks_cancel_func()
                    
                    text = await queue.get()
                else:
                    text = await asyncio.wait_for(queue.get(), timeout=self.timeout)
        except asyncio.TimeoutError:
            return text
        except Exception as e:
            logging.error(f"Error in speech: {e}")
            raise e
        finally:
            task.cancel()
            await self.funasr.receive().aclose()
            self.funasr.status = False
            
            
    async def run(self) -> str:
        logging.info("Collecting user speech...")
        text = await self.speech()
        logging.info(f"Recognized text: {text}")
        
        # 发送问题
        await self.send_question(text)

        return text
    