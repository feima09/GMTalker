import os
import yaml

home_dir = os.getcwd()


def get_preset_configs(config_type):
    """获取指定类型的预设配置文件列表"""
    config_dir = f"{home_dir}/configs/{config_type}"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    preset_files = [f for f in os.listdir(config_dir) if f.endswith(".yaml")]
    return preset_files


def load_preset_config(config_type, preset_file):
    """加载预设配置"""
    if not preset_file:
        return None, "请选择预设配置文件"
    
    preset_path = f"{home_dir}/configs/{config_type}/{preset_file}"
    if not os.path.exists(preset_path):
        return None, f"预设配置文件 {preset_file} 不存在"
    
    try:
        with open(preset_path, 'r', encoding='utf-8') as file:
            preset_config = yaml.safe_load(file)
            return preset_config, f"成功加载预设配置：{preset_file}"
    except Exception as e:
        return None, f"加载预设配置失败：{str(e)}"
    

def save_preset_config(config_type, config_data, file_name):
    """保存预设配置"""
    if not file_name:
        return "请输入预设配置文件名"
    
    if not file_name.endswith(".yaml"):
        file_name += ".yaml"
    
    preset_dir = f"{home_dir}/configs/{config_type}"
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)
    
    preset_path = f"{preset_dir}/{file_name}"
    
    try:
        with open(preset_path, 'w', encoding='utf-8') as file:
            yaml.dump(config_data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return f"预设配置已保存为 {file_name}"
    except Exception as e:
        return f"保存预设配置失败：{str(e)}"
    
