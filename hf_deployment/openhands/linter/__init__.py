"""Linter module for OpenHands.

Part of this Linter module is adapted from Aider (Apache 2.0 License, [original
code](https://github.com/paul-gauthier/aider/blob/main/aider/linter.py)).
- Please see the [original repository](https://github.com/paul-gauthier/aider) for more information.
- The detailed implementation of the linter can be found at: https://github.com/All-Hands-AI/openhands-aci.
"""

try:
    from openhands_aci.linter import DefaultLinter, LintResult
    LINTER_AVAILABLE = True
except ImportError:
    # Fallback implementation for when openhands_aci is not available
    class DefaultLinter:
        """Fallback linter that does nothing when openhands_aci is not available."""
        
        def __init__(self, *args, **kwargs):
            pass
        
        def lint(self, *args, **kwargs):
            """Return empty list when linting is not available."""
            return []
        
        def get_rel_fname(self, fname):
            """Fallback method for relative filename."""
            return fname
        
        def set_linter(self, linter):
            """Fallback method for setting linter."""
            pass
    
    class LintResult:
        """Fallback LintResult that mimics the real implementation structure."""
        
        def __init__(self, file_path=None, line_number=None, severity=None, message=None, 
                     rule=None, column=None, **kwargs):
            self.file_path = file_path
            self.line_number = line_number
            self.severity = severity or "info"
            self.message = message or ""
            self.rule = rule
            self.column = column
            # Store any additional kwargs as attributes
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def __repr__(self):
            return f"LintResult(file_path={self.file_path}, line_number={self.line_number}, severity={self.severity}, message={self.message})"
        
        def dict(self):
            """Mimic Pydantic's dict() method."""
            return {
                'file_path': self.file_path,
                'line_number': self.line_number,
                'severity': self.severity,
                'message': self.message,
                'rule': self.rule,
                'column': self.column
            }
        
        def model_dump(self):
            """Mimic Pydantic's model_dump() method."""
            return self.dict()
    
    LINTER_AVAILABLE = False

__all__ = ['DefaultLinter', 'LintResult', 'LINTER_AVAILABLE']
