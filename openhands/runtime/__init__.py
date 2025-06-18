from openhands.runtime.base import Runtime
from openhands.runtime.impl.cli.cli_runtime import CLIRuntime
from openhands.utils.import_utils import get_impl

# HF Spaces compatible imports with fallbacks
try:
    from openhands.runtime.impl.docker.docker_runtime import DockerRuntime
    DOCKER_AVAILABLE = True
except ImportError:
    # Fallback when docker is not available (e.g., in HF Spaces)
    class DockerRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("DockerRuntime requires docker package. Use CLIRuntime instead.")
    DOCKER_AVAILABLE = False

try:
    from openhands.runtime.impl.e2b.e2b_runtime import E2BRuntime
    E2B_AVAILABLE = True
except ImportError:
    class E2BRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("E2BRuntime requires e2b package. Use CLIRuntime instead.")
    E2B_AVAILABLE = False

try:
    from openhands.runtime.impl.local.local_runtime import LocalRuntime
    LOCAL_AVAILABLE = True
except ImportError:
    class LocalRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("LocalRuntime requires docker dependencies. Use CLIRuntime instead.")
    LOCAL_AVAILABLE = False

try:
    from openhands.runtime.impl.daytona.daytona_runtime import DaytonaRuntime
    DAYTONA_AVAILABLE = True
except ImportError:
    class DaytonaRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("DaytonaRuntime not available. Use CLIRuntime instead.")
    DAYTONA_AVAILABLE = False

try:
    from openhands.runtime.impl.modal.modal_runtime import ModalRuntime
    MODAL_AVAILABLE = True
except ImportError:
    class ModalRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("ModalRuntime not available. Use CLIRuntime instead.")
    MODAL_AVAILABLE = False

try:
    from openhands.runtime.impl.remote.remote_runtime import RemoteRuntime
    REMOTE_AVAILABLE = True
except ImportError:
    class RemoteRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("RemoteRuntime not available. Use CLIRuntime instead.")
    REMOTE_AVAILABLE = False

try:
    from openhands.runtime.impl.runloop.runloop_runtime import RunloopRuntime
    RUNLOOP_AVAILABLE = True
except ImportError:
    class RunloopRuntime:
        def __init__(self, *args, **kwargs):
            raise ImportError("RunloopRuntime not available. Use CLIRuntime instead.")
    RUNLOOP_AVAILABLE = False

# mypy: disable-error-code="type-abstract"
# HF Spaces compatible runtime classes - fallback to CLIRuntime when dependencies not available
_DEFAULT_RUNTIME_CLASSES: dict[str, type[Runtime]] = {
    'eventstream': CLIRuntime,  # Use CLI instead of Docker for HF Spaces
    'docker': CLIRuntime,       # Use CLI instead of Docker for HF Spaces
    'e2b': E2BRuntime if E2B_AVAILABLE else CLIRuntime,
    'remote': RemoteRuntime if REMOTE_AVAILABLE else CLIRuntime,
    'modal': ModalRuntime if MODAL_AVAILABLE else CLIRuntime,
    'runloop': RunloopRuntime if RUNLOOP_AVAILABLE else CLIRuntime,
    'local': CLIRuntime,        # Use CLI instead of Local for HF Spaces
    'daytona': DaytonaRuntime if DAYTONA_AVAILABLE else CLIRuntime,
    'cli': CLIRuntime,
}


def get_runtime_cls(name: str) -> type[Runtime]:
    """
    If name is one of the predefined runtime names (e.g. 'docker'), return its class.
    Otherwise attempt to resolve name as subclass of Runtime and return it.
    Raise on invalid selections.
    """
    if name in _DEFAULT_RUNTIME_CLASSES:
        return _DEFAULT_RUNTIME_CLASSES[name]
    try:
        return get_impl(Runtime, name)
    except Exception as e:
        known_keys = _DEFAULT_RUNTIME_CLASSES.keys()
        raise ValueError(
            f'Runtime {name} not supported, known are: {known_keys}'
        ) from e


__all__ = [
    'Runtime',
    'E2BRuntime',
    'RemoteRuntime',
    'ModalRuntime',
    'RunloopRuntime',
    'DockerRuntime',
    'DaytonaRuntime',
    'CLIRuntime',
    'get_runtime_cls',
]
