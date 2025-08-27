from typing import Dict, List
from .utils import ProcessManager
from utils import config

# 设置刷新时间间隔(秒)
REFRESH_INTERVAL = 1
max_log_lines = 1000  # 最大保留日志行数
log_lines: Dict[str, List[str]] = {}


def update_logs(process: ProcessManager) -> str:
    """
    更新并获取最新日志
    
    Returns:
        str: 格式化的日志文本
    """
    process_name = process.process_name
    global log_lines
    
    if log_lines.get(process_name, None) is None:
        log_lines[process_name] = ["等待服务启动..."]
    
    # 获取新日志
    new_logs = process.get_logs()
    if new_logs:
        log_lines[process_name].extend(new_logs)
        if len(log_lines[process_name]) > max_log_lines:
            log_lines[process_name] = log_lines[process_name][-max_log_lines:]
    
    # 返回格式化的日志文本
    return "\n".join(log_lines[process_name])


def get_status(process: ProcessManager) -> Dict[str, str]:
    """
    获取并格式化后端状态信息
    
    Returns:
        Dict[str, str]: 格式化后的状态信息
    """
    status_info = process.get_status()
    
    # 格式化运行时间
    uptime = status_info["uptime"]
    if uptime > 0:
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        uptime_str = f"{hours}小时 {minutes}分钟 {seconds}秒"
    else:
        uptime_str = "0秒"
    
    return {
        "状态": status_info["status"],
        "运行时间": uptime_str,
        "内存使用": f"{status_info['memory_mb']} MB",
        "CPU使用": f"{status_info['cpu_percent']}%",
        "进程ID": str(status_info["pid"] or "无")
    }


def clear_logs(process: ProcessManager) -> str:
    """
    清空日志显示
    
    Returns:
        str: 空字符串，用于清空日志区域
    """
    global log_lines
    if log_lines.get(process.process_name, None) is not None:
        log_lines[process.process_name] = []
    return ""


def save_config(field: str, value: str) -> str:
    """
    保存配置到配置文件
    
    Args:
        field (str): 配置字段名称
        value (str): 配置值
    
    Returns:
        str: 成功消息
    """
    Config = config.Webui
    
    Config[field] = value
    config.save_config(Config, "webui.yaml")
    return f"{field}已保存为: {value}"

