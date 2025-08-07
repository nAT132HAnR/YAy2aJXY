# 代码生成时间: 2025-08-07 14:27:46
import json
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, abort
from wtforms import Form, StringField, validators, ValidationError

# 定义一个表单数据验证器类
class FormValidator:
    def __init__(self, req: Request):
        self.req = req
        self.form = Form()  # 创建一个空表单

    def validate_data(self, schema: dict) -> dict:
        """
        验证表单数据，schema格式为字段名对应验证器的字典。
        :param schema: 验证规则字典。
        :return: 验证通过的数据字典。
        """
        try:
            data = json.loads(self.req.json)  # 解析请求体为JSON
            for field, validators_list in schema.items():
                field_value = data.get(field)
                if field_value is None:
                    raise ValidationError(f"{field} is required")
                for validator in validators_list:
                    if not validator(field_value):
                        raise ValidationError(f"{field} validation error")
            return data
        except json.JSONDecodeError:
            abort(400, 'Invalid JSON format')
        except ValidationError as e:
            abort(400, str(e))

# 创建一个Sanic应用
app = Sanic('FormValidatorApp')

# 定义一个路由处理POST请求
@app.route('/validate_form', methods=['POST'])
async def validate_form(request: Request):
    # 创建表单验证器实例
    validator = FormValidator(request)
    # 定义验证规则
    schema = {
        'name': [validators.Length(min=2, max=50)],
        'email': [validators.Email()],
        'age': [lambda x: x.isdigit() and 0 < int(x) < 130]
    }
    try:
        # 执行验证并返回结果
        valid_data = validator.validate_data(schema)
        return response.json(valid_data)
    except ServerError as e:
        return response.json(str(e), status=e.status_code)

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)