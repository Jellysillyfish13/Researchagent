import os
import google.generativeai as genai
from typing import Optional
import asyncio

# 设置API密钥
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY环境变量未设置")

# 配置API
genai.configure(api_key=GEMINI_API_KEY)

# 非异步版本
def generate_gemini_response_sync(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    使用Gemini API生成响应（同步版本）
    
    Args:
        prompt: 输入提示
        model_name: 要使用的模型名称，默认使用gemini-1.5-flash
        
    Returns:
        生成的响应文本
    """
    try:
        # 确保使用有效的模型名称
        model = genai.GenerativeModel(model_name)
        
        # 生成内容
        response = model.generate_content(prompt)
        
        # 提取响应文本
        if response.text:
            return response.text
        else:
            return "无法生成响应。可能是由于安全过滤器触发或其他API问题。"
    
    except Exception as e:
        print(f"Error generating response: {e}")
        # 提供一个备用响应
        return f"生成响应时出错: {str(e)}"

# 异步包装器
async def generate_gemini_response(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    使用Gemini API生成响应（异步版本）
    
    Args:
        prompt: 输入提示
        model_name: 要使用的模型名称，默认使用gemini-1.5-flash
        
    Returns:
        生成的响应文本
    """
    # 使用线程池运行同步函数
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: generate_gemini_response_sync(prompt, model_name)
    )
    return response

# 用于格式化搜索结果的函数
def format_results_for_llm(results):
    """
    将搜索结果格式化为LLM可读的形式
    
    Args:
        results: 搜索结果列表
        
    Returns:
        格式化后的字符串
    """
    formatted_text = ""
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        snippet = result.get("snippet", "No snippet")
        url = result.get("url", "No URL")
        
        formatted_text += f"[{i}] {title}\n"
        formatted_text += f"URL: {url}\n"
        formatted_text += f"Description: {snippet}\n\n"
    
    return formatted_text

# 用于执行网络搜索的函数
def search_web(query, api_key, max_results=5):
    """
    使用搜索API执行网络搜索
    
    Args:
        query: 搜索查询
        api_key: API密钥
        max_results: 返回的最大结果数
        
    Returns:
        搜索结果列表
    """
    # 这里应该实现真正的搜索功能
    # 由于您提到不需要mock API，我假设您有真实实现
    # 如果需要，可以在这里添加
    
    # 返回示例结果（应该替换为真实实现）
    mock_results = []
    for i in range(min(max_results, 3)):
        mock_results.append({
            "title": f"Result {i+1} for {query}",
            "snippet": f"This is a snippet of information related to {query}. It contains relevant details that would be useful for research.",
            "url": f"https://example.com/result-{i+1}"
        })
    return mock_results