"""
Inference System - Forward-chaining inference engine and knowledge base
This is the AI reasoning system
"""

from .inference_engine import InferenceEngine
from .rule import Rule
from .knowledge_base import KnowledgeBase

__all__ = [
    'InferenceEngine',
    'Rule',
    'KnowledgeBase',
]
