"""
Prompt Optimizer Module for FMBench

This module uses the AWS Bedrock Agent Runtime to optimize prompts for different models.
"""

import boto3
import logging
import time
from typing import Dict, Optional, List, Union, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptOptimizer:
    """
    Optimizes prompts for different model types using Bedrock Agent Runtime.
    """
    def __init__(self, region: Optional[str] = None):
        """
        Initialize the PromptOptimizer.
        
        Args:
            region: AWS region for Bedrock. If None, uses default boto3 region.
        """
        self.client = boto3.client('bedrock-agent-runtime', region_name=region)
        
        # Comprehensive mapping of Bedrock model IDs to target model IDs for optimization
        # This allows us to match exact model IDs from benchmarking configs
        self.model_id_map = {
            # Claude models - optimize using Claude 3 Sonnet
            "anthropic.claude-instant-v1": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-v1": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-v2": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-v2:1": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
            
            # Llama models - optimize using Llama 3
            "meta.llama2-13b-chat-v1": "meta.llama3-70b-instruct-v1:0",
            "meta.llama2-70b-chat-v1": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-8b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-70b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-1-8b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-1-70b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-1-405b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-1b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-3b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-11b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-90b-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-11b-vision-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-2-90b-vision-instruct-v1:0": "meta.llama3-70b-instruct-v1:0",
            
            # Mistral models - optimize using Mistral Large
            "mistral.mistral-7b-instruct-v0:2": "mistral.mistral-large-2402-v1:0",
            "mistral.mistral-large-2402-v1:0": "mistral.mistral-large-2402-v1:0",
            "mistral.mistral-large-2405-v1:0": "mistral.mistral-large-2402-v1:0",
            "mistral.mixtral-8x7b-instruct-v0:1": "mistral.mistral-large-2402-v1:0",
            "mistral.mistral-small-2402-v1:0": "mistral.mistral-large-2402-v1:0",
            "mistral.mistral-medium-2312-v1:0": "mistral.mistral-large-2402-v1:0",
            
            # Amazon models - optimize using Titan
            "amazon.titan-text-lite-v1": "amazon.titan-text-express-v1:0",
            "amazon.titan-text-express-v1": "amazon.titan-text-express-v1:0",
            "amazon.titan-text-express-v1:0": "amazon.titan-text-express-v1:0",
            "amazon.titan-text-premier-v1:0": "amazon.titan-text-express-v1:0",
            "amazon.titan-embed-text-v1": "amazon.titan-text-express-v1:0",
            "amazon.titan-embed-image-v1": "amazon.titan-text-express-v1:0",
            "amazon.titan-multimodal-embeddings-v1:0": "amazon.titan-text-express-v1:0",
            "amazon.titan-image-generator-v1:0": "amazon.titan-text-express-v1:0",
            "amazon.titan-image-generator-v21:0": "amazon.titan-text-express-v1:0",
            
            # Cohere models - optimize using Command
            "cohere.command-text-v14": "cohere.command-text-v14:5:0",
            "cohere.command-text-v14:5:0": "cohere.command-text-v14:5:0",
            "cohere.command-light-text-v14:5:0": "cohere.command-text-v14:5:0",
            "cohere.command-r-text-v1:0": "cohere.command-text-v14:5:0",
            "cohere.command-r-plus-text-v1:0": "cohere.command-text-v14:5:0",
            "cohere.embed-english-v3": "cohere.command-text-v14:5:0",
            "cohere.embed-multilingual-v3": "cohere.command-text-v14:5:0",
            
            # Other models - fallback to appropriate formats
            "ai21.j2-mid-v1": "anthropic.claude-3-sonnet-20240229-v1:0",
            "ai21.j2-ultra-v1": "anthropic.claude-3-sonnet-20240229-v1:0",
            "ai21.jamba-instruct-v1:0": "anthropic.claude-3-sonnet-20240229-v1:0",
            "stability.stable-diffusion-xl-v0": "amazon.titan-text-express-v1:0",
            "stability.stable-diffusion-xl-v1": "amazon.titan-text-express-v1:0"
        }
        
        # Generic family mapping as fallback if exact model ID isn't found
        self.family_map = {
            "anthropic": "anthropic.claude-3-sonnet-20240229-v1:0",
            "claude": "anthropic.claude-3-sonnet-20240229-v1:0",
            "mistral": "mistral.mistral-large-2402-v1:0",
            "llama": "meta.llama3-70b-instruct-v1:0",
            "meta": "meta.llama3-70b-instruct-v1:0",
            "nova": "amazon.titan-text-express-v1:0",
            "titan": "amazon.titan-text-express-v1:0",
            "amazon": "amazon.titan-text-express-v1:0",
            "cohere": "cohere.command-text-v14:5:0",
            "command": "cohere.command-text-v14:5:0",
            "ai21": "anthropic.claude-3-sonnet-20240229-v1:0",
            "stability": "amazon.titan-text-express-v1:0",
            "deepseek": "anthropic.claude-3-sonnet-20240229-v1:0"
        }
        
        # Cache optimized prompts to avoid repeated API calls
        self.prompt_cache = {}

    def _get_target_model_id(self, model_id: str) -> str:
        """
        Get the target model ID for optimization by first checking for exact matches,
        then falling back to family detection.
        
        Args:
            model_id: The exact model ID from the benchmarking config
            
        Returns:
            Bedrock model ID to use for optimization
        """
        # Try direct lookup first - this handles exact model IDs used in benchmarking
        if model_id in self.model_id_map:
            logger.info(f"Found exact match for model ID: {model_id}")
            return self.model_id_map[model_id]
        
        # If no exact match, try to determine the model family
        model_id_lower = model_id.lower()
        
        # Find the right family by checking for keywords in the model ID
        for family, target_id in self.family_map.items():
            if family in model_id_lower:
                logger.info(f"Matched model ID {model_id} to family {family}")
                return target_id
        
        # Default to Claude format if unknown - this is a good general choice
        logger.warning(f"Unknown model ID: {model_id}. Using Claude format as fallback.")
        return self.family_map["claude"]

    def optimize_prompt(self, 
                       prompt: str, 
                       model_id: str, 
                       retry_count: int = 3) -> Tuple[str, Optional[str]]:
        """
        Optimize a prompt for a specific model.
        
        Args:
            prompt: The original prompt text
            model_id: The exact model ID from the benchmarking config
            retry_count: Number of retries if the API call fails
            
        Returns:
            Tuple of (optimized prompt, analysis)
        """
        # Generate a cache key based on the prompt and model_id
        cache_key = f"{model_id}:{prompt}"
        
        # Check if result is already in cache
        if cache_key in self.prompt_cache:
            logger.info(f"Using cached optimized prompt for model {model_id}")
            return self.prompt_cache[cache_key]
         
        # Get the appropriate target model for optimization  
        target_model_id = self._get_target_model_id(model_id)
        
        logger.info(f"Optimizing prompt for model: {model_id} using target model: {target_model_id}")
        
        optimized_prompt = prompt
        analysis = None
        
        # Only call the API if the model ID is different from the target 
        # (i.e., don't optimize claude-sonnet for claude-sonnet, but do optimize llama for llama)
        if model_id != target_model_id:
            for attempt in range(retry_count):
                try:
                    response = self.client.optimize_prompt(
                        input={"textPrompt": {"text": prompt}},
                        targetModelId=target_model_id
                    )
                    
                    # Process the response
                    for event in response.get('optimizedPrompt', []):
                        if 'optimizedPromptEvent' in event:
                            optimized_prompt = event['optimizedPromptEvent']
                        elif 'analyzePromptEvent' in event:
                            analysis = event['analyzePromptEvent']
                    
                    # Cache the result
                    self.prompt_cache[cache_key] = (optimized_prompt, analysis)
                    return optimized_prompt, analysis
                
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1}/{retry_count} failed to optimize prompt: {str(e)}")
                    if attempt < retry_count - 1:
                        # Exponential backoff
                        time.sleep(2 ** attempt)
                    else:
                        logger.error(f"Failed to optimize prompt after {retry_count} attempts. Using original prompt.")
        else:
            logger.info(f"Model {model_id} is already a target model. No optimization needed.")
        
        # If we reach here, return the original prompt
        self.prompt_cache[cache_key] = (optimized_prompt, analysis)
        return optimized_prompt, analysis