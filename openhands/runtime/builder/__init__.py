from openhands.runtime.builder.base import RuntimeBuilder

# HF Spaces compatible import
try:
    from openhands.runtime.builder.docker import DockerRuntimeBuilder
    __all__ = ['RuntimeBuilder', 'DockerRuntimeBuilder']
except ImportError:
    # Fallback when docker is not available
    __all__ = ['RuntimeBuilder']
