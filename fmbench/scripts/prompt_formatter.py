"""
Prompt Formatter for FMBench

This module integrates with the AWS Bedrock Agent Runtime to 
optimize prompts for different model types.
"""

import logging
import boto3
from typing import Dict, Optional
from fmbench.scripts.prompt_optimizer import PromptOptimizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptFormatter:
    """
    Formats prompts for different model types using the Bedrock Agent Runtime optimize_prompt API.
    """
    def __init__(self, region: Optional[str] = None):
        """
        Initialize the PromptFormatter.
        
        Args:
            region: AWS region for Bedrock. If None, uses default boto3 region.
        """
        self.optimizer = PromptOptimizer(region)
        self.formatted_prompt_cache = {}

    def format_prompt_for_model(self, payload: Dict, model_id: str) -> Dict:
        """
        Format a prompt for a specific model type.
        
        Args:
            payload: The payload dictionary containing the prompt
            model_id: The exact model ID from the benchmarking config
            
        Returns:
            Updated payload with optimized prompt
        """
        # Create a deep copy of the payload to avoid modifying the original
        new_payload = payload.copy()
        
        # Skip if there's no prompt
        if "inputs" not in new_payload:
            logger.warning(f"No 'inputs' found in payload: {new_payload}")
            return new_payload
            
        prompt = new_payload["inputs"]
        
        # Generate a cache key based on the prompt and model_id
        cache_key = f"{model_id}:{prompt}"
        
        # Check if already formatted
        if cache_key in self.formatted_prompt_cache:
            logger.info(f"Using cached formatted prompt for model {model_id}")
            new_payload["inputs"] = self.formatted_prompt_cache[cache_key]
            new_payload["original_inputs"] = prompt
            return new_payload
        
        # Optimize the prompt
        try:
            logger.info(f"Optimizing prompt for Bedrock model: {model_id}")
            
            # Short prompt preview (first 50 chars)
            prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
            logger.info(f"Original prompt (preview): {prompt_preview}")
            
            optimized_prompt, analysis = self.optimizer.optimize_prompt(prompt, model_id)
            
            # Check if optimization actually changed the prompt
            if optimized_prompt != prompt:
                logger.info(f"Prompt was optimized for model {model_id}")
                # Short optimized prompt preview
                opt_preview = optimized_prompt[:50] + "..." if len(optimized_prompt) > 50 else optimized_prompt
                logger.info(f"Optimized prompt (preview): {opt_preview}")
            else:
                logger.info(f"Prompt was not changed for model {model_id}")
            
            # Cache the result
            self.formatted_prompt_cache[cache_key] = optimized_prompt
            
            # Update the payload
            new_payload["inputs"] = optimized_prompt
            new_payload["original_inputs"] = prompt
            
            if analysis:
                logger.info(f"Prompt analysis: {analysis}")
                
        except Exception as e:
            logger.error(f"Error formatting prompt for model {model_id}: {e}")
            # Return the original payload if optimization fails
            return payload
            
        return new_payload

# Singleton instance to be used throughout the application
formatter = PromptFormatter()