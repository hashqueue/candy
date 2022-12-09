import logging
import json
import traceback

import psutil
from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger('my_debug_logger')


class ServerPerformanceConsumer(WebsocketConsumer):

    def receive(self, text_data=None, bytes_data=None):
        # logger.debug(self.scope)
        try:
            message = json.loads(text_data)
            if message.get('action') == 'get-performance-data':
                # 获取服务器性能相关数据
                cpu_count = psutil.cpu_count()
                cpu_percent = psutil.cpu_percent()
                virtual_memory = psutil.virtual_memory()
                total_memory = eval(f'{(virtual_memory.total / 1024 / 1024 / 1024):.2f}')
                available_memory = eval(f'{(virtual_memory.available / 1024 / 1024 / 1024):.2f}')
                free_memory = eval(f'{(virtual_memory.free / 1024 / 1024 / 1024):.2f}')
                used_memory = eval(f'{((virtual_memory.total - virtual_memory.free) / 1024 / 1024 / 1024):.2f}')
                percent_memory = eval(
                    f'{((virtual_memory.total - virtual_memory.available) / virtual_memory.total * 100):.2f}')
                disk_info = psutil.disk_usage('/')
                total_disk = eval(f'{disk_info.total / 1024 / 1024 / 1024:.2f}')
                used_disk = eval(f'{disk_info.used / 1024 / 1024 / 1024:.2f}')
                free_disk = eval(f'{disk_info.free / 1024 / 1024 / 1024:.2f}')
                percent_disk = disk_info.percent
                server_data = {
                    'cpu': {'cpu_count': cpu_count, 'cpu_percent': cpu_percent},
                    'memory': {
                        'total_memory': total_memory, 'available_memory': available_memory, 'free_memory': free_memory,
                        'used_memory': used_memory, 'percent_memory': percent_memory
                    },
                    'disk': {
                        'total_disk': total_disk, 'used_disk': used_disk, 'free_disk': free_disk,
                        'percent_disk': percent_disk
                    }
                }
                self.send(json.dumps({"data": server_data}))
        except Exception as err:
            logger.error(f'error when deal message from ws client: text_data is <{text_data}>, error is <{err}>, '
                         f'traceback is <{traceback.format_exc()}>.')
