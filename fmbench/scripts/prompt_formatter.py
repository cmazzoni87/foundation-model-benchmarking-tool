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
            logger.warning(f"No 'inputs' found in payload")
            return new_payload
            
        prompt = new_payload["inputs"]
        
        # Optimize the prompt
        try:
            # Optimization is handled (including caching) by the optimizer
            optimized_prompt, _ = self.optimizer.optimize_prompt(prompt, model_id)
            
            # Only log if prompt was changed
            if optimized_prompt != prompt:
                logger.info(f"Prompt optimized for model {model_id}")
            
            # Update the payload
            new_payload["inputs"] = optimized_prompt
            new_payload["original_inputs"] = prompt
                
        except Exception as e:
            logger.error(f"Error formatting prompt for model {model_id}: {e}")
            # Return the original payload if optimization fails
            return payload
            
        return new_payload

# Singleton instance to be used throughout the application
formatter = PromptFormatter()