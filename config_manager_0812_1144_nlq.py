# 代码生成时间: 2025-08-12 11:44:23
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import HTTPResponse


# 配置文件管理器
class ConfigManager:
    def __init__(self, config_path):
        """初始化配置文件管理器
        
        参数:
        config_path (str): 配置文件路径
        """
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        """加载配置文件
        
        返回:
        dict: 配置数据
        
        异常:
        FileNotFoundError: 如果配置文件不存在
        """
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ServerError('配置文件不存在', status_code=404)

    def save_config(self):
        """保存配置到文件
        
        异常:
        PermissionError: 如果没有写入权限
        """
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        except PermissionError:
            raise ServerError('没有写入权限', status_code=403)

    def get_config(self):
        """获取配置数据
        
        返回:
        dict: 配置数据
        """
        return self.config_data

    def update_config(self, key, value):
        """更新配置数据
        
        参数:
        key (str): 配置项键
        value (any): 配置项值
        
        异常:
        KeyError: 如果配置项不存在
        """
        try:
            self.config_data[key] = value
            self.save_config()
        except KeyError:
            raise ServerError('配置项不存在', status_code=404)


# Sanic 应用
app = Sanic('ConfigManagerApp')
config_manager = ConfigManager('config.json')

@app.get('/config')
async def get_config(request: Request):
    """获取配置数据
    
    返回:
    配置数据
    """
    return response.json(config_manager.get_config())

@app.put('/config/<key>')
async def update_config(request: Request, key: str):
    """更新配置数据
    
    参数:
    key (str): 配置项键
    
    返回:
    更新后的配置数据
    
    异常:
    400: 如果请求体为空
    404: 如果配置项不存在
    """
    if not request.json:
        return response.json({'error': '请求体不能为空'}, status=400)
    value = request.json.get('value')
    if value is None:
        return response.json({'error': 'value不能为空'}, status=400)
    try:
        config_manager.update_config(key, value)
    except ServerError as e:
        return response.json({'error': str(e)}, status=e.status_code)
    return response.json(config_manager.get_config())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)