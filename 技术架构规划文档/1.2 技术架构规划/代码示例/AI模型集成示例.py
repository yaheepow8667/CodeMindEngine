# AI模型集成示例

# 1. 后端AI服务层实现（ai_service.py）

import os
import logging
import asyncio
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

import openai
import requests
from fastapi import HTTPException
from cachetools import TTLCache

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置缓存
ai_cache = TTLCache(maxsize=1000, ttl=3600)  # 缓存1小时

# 模型配置
MODEL_CONFIG = {
    "gpt-4o": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": "https://api.openai.com/v1",
        "temperature": 0.7,
        "max_tokens": 8192,
        "stop_sequences": ["\n\n", "</code>", "</form>"]
    },
    "codellama": {
        "api_key": os.getenv("CODELLAMA_API_KEY"),
        "base_url": "https://api.codellama.com/v1",
        "temperature": 0.5,
        "max_tokens": 16384,
        "stop_sequences": ["\n\n", "</code>", "```"]
    }
}

# 模型适配器抽象类
class ModelAdapter(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def generate_code(self, prompt: str, language: str, **kwargs) -> str:
        pass

# GPT模型适配器
class GPTAdapter(ModelAdapter):
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.config = MODEL_CONFIG.get(model_name)
        if not self.config:
            raise ValueError(f"未知的模型名称: {model_name}")
        
        # 配置OpenAI客户端
        self.client = openai.AsyncOpenAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"]
        )

    async def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个专业的AI助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", self.config["temperature"]),
                max_tokens=kwargs.get("max_tokens", self.config["max_tokens"]),
                stop=kwargs.get("stop_sequences", self.config["stop_sequences"])
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"GPT模型调用失败: {str(e)}")
            raise HTTPException(status_code=500, detail="AI模型调用失败")

    async def generate_code(self, prompt: str, language: str, **kwargs) -> str:
        try:
            code_prompt = f"请生成{language}代码实现以下功能：\n{prompt}\n\n只返回代码部分，不要包含解释。"
            return await self.generate_text(code_prompt, **kwargs)
        except Exception as e:
            logger.error(f"GPT代码生成失败: {str(e)}")
            raise HTTPException(status_code=500, detail="代码生成失败")

# CodeLlama模型适配器
class CodeLlamaAdapter(ModelAdapter):
    def __init__(self, model_name: str = "codellama"):
        self.model_name = model_name
        self.config = MODEL_CONFIG.get(model_name)
        if not self.config:
            raise ValueError(f"未知的模型名称: {model_name}")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = requests.post(
                f"{self.config['base_url']}/completions",
                headers={
                    "Authorization": f"Bearer {self.config['api_key']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "codellama/CodeLlama-34b-Instruct-hf",
                    "prompt": prompt,
                    "temperature": kwargs.get("temperature", self.config["temperature"]),
                    "max_tokens": kwargs.get("max_tokens", self.config["max_tokens"]),
                    "stop": kwargs.get("stop_sequences", self.config["stop_sequences"])
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"CodeLlama模型调用失败: {str(e)}")
            raise HTTPException(status_code=500, detail="AI模型调用失败")

    async def generate_code(self, prompt: str, language: str, **kwargs) -> str:
        try:
            code_prompt = f"<s>[INST] 请生成{language}代码实现以下功能：\n{prompt}\n\n只返回代码部分，不要包含解释。 [/INST]"
            return await self.generate_text(code_prompt, **kwargs)
        except Exception as e:
            logger.error(f"CodeLlama代码生成失败: {str(e)}")
            raise HTTPException(status_code=500, detail="代码生成失败")

# AI服务管理器
class AIServiceManager:
    def __init__(self):
        self.adapters = {
            "gpt-4o": GPTAdapter(),
            "codellama": CodeLlamaAdapter()
        }

    def get_adapter(self, model_name: str) -> ModelAdapter:
        adapter = self.adapters.get(model_name)
        if not adapter:
            raise ValueError(f"不支持的模型: {model_name}")
        return adapter

    async def generate_text(self, prompt: str, model_name: str = "gpt-4o", **kwargs) -> str:
        # 检查缓存
        cache_key = f"text:{model_name}:{prompt}"
        if cache_key in ai_cache:
            return ai_cache[cache_key]

        adapter = self.get_adapter(model_name)
        result = await adapter.generate_text(prompt, **kwargs)
        
        # 保存到缓存
        ai_cache[cache_key] = result
        return result

    async def generate_code(self, prompt: str, language: str, model_name: str = "codellama", **kwargs) -> str:
        # 检查缓存
        cache_key = f"code:{model_name}:{language}:{prompt}"
        if cache_key in ai_cache:
            return ai_cache[cache_key]

        adapter = self.get_adapter(model_name)
        result = await adapter.generate_code(prompt, language, **kwargs)
        
        # 保存到缓存
        ai_cache[cache_key] = result
        return result

    async def generate_form(self, requirements: str, framework: str = "vue3", ui_library: str = "element-plus", **kwargs) -> Dict[str, Any]:
        prompt = f"请生成一个{framework} + {ui_library}的表单组件，满足以下需求：\n{requirements}\n\n请返回完整的组件代码，包括模板、脚本和样式部分。"
        
        code = await self.generate_code(prompt, "vue", model_name="gpt-4o", **kwargs)
        
        # 提取不同部分的代码
        # 这里简化处理，实际项目中需要更复杂的代码解析
        return {
            "component_code": code,
            "validation_code": "",  # 需要从生成的代码中提取
            "preview_html": "",  # 需要转换生成的代码为HTML
            "suggestions": []  # 可以根据生成结果提供优化建议
        }

    async def generate_page(self, requirements: str, framework: str = "vue3", ui_library: str = "element-plus", **kwargs) -> Dict[str, Any]:
        prompt = f"请生成一个{framework} + {ui_library}的页面组件，满足以下需求：\n{requirements}\n\n请返回完整的组件代码，包括模板、脚本和样式部分。"
        
        code = await self.generate_code(prompt, "vue", model_name="gpt-4o", **kwargs)
        
        return {
            "template_code": code,  # 需要从生成的代码中提取
            "script_code": "",  # 需要从生成的代码中提取
            "style_code": "",  # 需要从生成的代码中提取
            "preview_html": "",  # 需要转换生成的代码为HTML
            "dependencies": []  # 需要分析生成代码的依赖
        }

    async def generate_api(self, database_schema: str, framework: str = "fastapi", **kwargs) -> Dict[str, Any]:
        prompt = f"请根据以下数据库表结构生成{framework}风格的API接口代码：\n{database_schema}\n\n请返回完整的API代码，包括路由、模型和CRUD操作。"
        
        code = await self.generate_code(prompt, "python", model_name="codellama", **kwargs)
        
        return {
            "router_code": code,  # 需要从生成的代码中提取
            "model_code": "",  # 需要从生成的代码中提取
            "crud_code": "",  # 需要从生成的代码中提取
            "documentation": ""  # 需要生成API文档
        }

# 创建全局AI服务管理器实例
ai_service_manager = AIServiceManager()

# 2. 前端AI服务调用示例（api/ai.js）

/*
import request from '@/utils/request'

// 智能表单生成
export function generateForm(data) {
  return request({
    url: '/api/v1/ai/generate-form',
    method: 'post',
    data
  })
}

// 智能页面生成
export function generatePage(data) {
  return request({
    url: '/api/v1/ai/generate-page',
    method: 'post',
    data
  })
}

// 智能API生成
export function generateApi(data) {
  return request({
    url: '/api/v1/ai/generate-api',
    method: 'post',
    data
  })
}

// 智能代码优化
export function optimizeCode(data) {
  return request({
    url: '/api/v1/ai/optimize-code',
    method: 'post',
    data
  })
}
*/
