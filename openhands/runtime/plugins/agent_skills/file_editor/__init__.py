"""This file imports a global singleton of the `EditTool` class as well as raw functions that expose
its __call__.
The implementation of the `EditTool` class can be found at: https://github.com/All-Hands-AI/openhands-aci/.
"""

try:
    from openhands_aci.editor import file_editor
except ImportError:
    # Fallback to local implementation for HF Spaces deployment
    from openhands.runtime.action_execution_server import _execute_file_editor
    
    def file_editor(command, path, file_text=None, old_str=None, new_str=None, insert_line=None, view_range=None):
        """Fallback file editor implementation using local action execution server."""
        from openhands.events.action import FileEditAction
        
        action = FileEditAction(
            command=command,
            path=path,
            file_text=file_text,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
            view_range=view_range
        )
        
        result, _ = _execute_file_editor(action)
        return result

__all__ = ['file_editor']
