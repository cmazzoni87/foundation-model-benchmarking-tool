from enum import Enum
from typing import List

# These variables represent the platform where a specific
# endpoint is deployed.
PLATFORM_BEDROCK: str = "bedrock"
PLATFORM_EXTERNAL: str = "external"

# This is the file where metrics are stored
SYSTEM_METRICS_FNAME: str = "System_metrics.csv"