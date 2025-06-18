"""
Runtime implementations for OpenHands.
"""

from openhands.runtime.impl.action_execution.action_execution_client import (
    ActionExecutionClient,
)
from openhands.runtime.impl.cli import CLIRuntime
from openhands.runtime.impl.local.local_runtime import LocalRuntime
from openhands.runtime.impl.remote.remote_runtime import RemoteRuntime

# Conditional E2B import for HF Spaces compatibility
try:
    from openhands.runtime.impl.e2b.e2b_runtime import E2BRuntime
    E2B_AVAILABLE = True
except ImportError:
    # Fallback when e2b is not available (e.g., in HF Spaces)
    class E2BRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("E2BRuntime requires e2b package. Use CLIRuntime or LocalRuntime instead.")
    E2B_AVAILABLE = False

# Conditional Docker import for HF Spaces compatibility
try:
    from openhands.runtime.impl.docker.docker_runtime import DockerRuntime
    DOCKER_AVAILABLE = True
except ImportError:
    # Fallback when docker is not available (e.g., in HF Spaces)
    class DockerRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("DockerRuntime requires docker package. Use E2BRuntime or LocalRuntime instead.")
    DOCKER_AVAILABLE = False

# Conditional imports for external services
try:
    from openhands.runtime.impl.daytona.daytona_runtime import DaytonaRuntime
    DAYTONA_AVAILABLE = True
except ImportError:
    # Fallback when daytona_sdk is not available
    class DaytonaRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("DaytonaRuntime requires daytona_sdk package")
    DAYTONA_AVAILABLE = False

try:
    from openhands.runtime.impl.modal.modal_runtime import ModalRuntime
    MODAL_AVAILABLE = True
except ImportError:
    # Fallback when modal is not available
    class ModalRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("ModalRuntime requires modal package")
    MODAL_AVAILABLE = False

try:
    from openhands.runtime.impl.runloop.runloop_runtime import RunloopRuntime
    RUNLOOP_AVAILABLE = True
except ImportError:
    # Fallback when runloop-api-client is not available
    class RunloopRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("RunloopRuntime requires runloop-api-client package")
    RUNLOOP_AVAILABLE = False

__all__ = [
    'ActionExecutionClient',
    'CLIRuntime',
    'DaytonaRuntime',
    'DockerRuntime',
    'E2BRuntime',
    'LocalRuntime',
    'ModalRuntime',
    'RemoteRuntime',
    'RunloopRuntime',
    'DAYTONA_AVAILABLE',
    'DOCKER_AVAILABLE',
    'E2B_AVAILABLE',
    'MODAL_AVAILABLE',
    'RUNLOOP_AVAILABLE',
]
