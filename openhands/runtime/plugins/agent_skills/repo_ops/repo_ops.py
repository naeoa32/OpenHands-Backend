try:
    from openhands_aci.indexing.locagent.tools import (
        explore_tree_structure,
        get_entity_contents,
        search_code_snippets,
    )
except ImportError:
    # Fallback implementations for HF Spaces
    import os
    import fnmatch
    from pathlib import Path
    from typing import List, Dict, Any
    
    def explore_tree_structure(path: str, max_depth: int = 3) -> Dict[str, Any]:
        """Fallback tree exploration."""
        def _explore(current_path: str, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth >= max_depth:
                return {}
            
            result = {}
            try:
                for item in os.listdir(current_path):
                    if item.startswith('.'):
                        continue
                    
                    item_path = os.path.join(current_path, item)
                    if os.path.isdir(item_path):
                        result[item] = _explore(item_path, current_depth + 1)
                    else:
                        result[item] = "file"
            except PermissionError:
                pass
            
            return result
        
        return _explore(path)
    
    def get_entity_contents(path: str, entity_name: str) -> str:
        """Fallback entity content retrieval."""
        try:
            full_path = os.path.join(path, entity_name)
            if os.path.isfile(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return f"Entity not found: {entity_name}"
        except Exception as e:
            return f"Error reading entity: {str(e)}"
    
    def search_code_snippets(path: str, query: str, file_pattern: str = "*.py") -> List[Dict[str, Any]]:
        """Fallback code search."""
        results = []
        try:
            for root, dirs, files in os.walk(path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if fnmatch.fnmatch(file, file_pattern):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    lines = content.splitlines()
                                    for i, line in enumerate(lines):
                                        if query.lower() in line.lower():
                                            results.append({
                                                "file": file_path,
                                                "line": i + 1,
                                                "content": line.strip(),
                                                "context": lines[max(0, i-2):i+3]
                                            })
                        except Exception:
                            continue
        except Exception:
            pass
        
        return results

__all__ = [
    'get_entity_contents',
    'search_code_snippets',
    'explore_tree_structure',
]
