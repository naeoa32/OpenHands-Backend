"""This file imports a global singleton of the `EditTool` class as well as raw functions that expose
its __call__.
The implementation of the `EditTool` class can be found at: https://github.com/All-Hands-AI/openhands-aci/.
"""

try:
    from openhands_aci.editor import file_editor
except ImportError:
    # Fallback to simple file operations for HF Spaces deployment
    import os
    
    def file_editor(command, path, file_text=None, old_str=None, new_str=None, insert_line=None, view_range=None):
        """Fallback file editor implementation for HF Spaces deployment."""
        try:
            if command == 'view':
                if os.path.isdir(path):
                    files = []
                    for root, dirs, filenames in os.walk(path):
                        level = root.replace(path, '').count(os.sep)
                        if level < 2:  # Only 2 levels deep
                            for f in filenames:
                                if not f.startswith('.'):
                                    files.append(os.path.join(root, f))
                            for d in dirs:
                                if not d.startswith('.'):
                                    files.append(os.path.join(root, d) + '/')
                    content = f"Here's the files and directories up to 2 levels deep in {path}, excluding hidden items:\n"
                    content += '\n'.join(sorted(files))
                    return content
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    if view_range:
                        start, end = view_range
                        lines = lines[start-1:end]
                    content = f"Here's the result of running `cat -n` on {path}:\n"
                    for i, line in enumerate(lines, 1):
                        content += f"{i:6}\t{line.rstrip()}\n"
                    return content
                    
            elif command == 'create':
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(file_text or '')
                return f"File created successfully at {path}"
                
            elif command == 'str_replace':
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_str not in content:
                    return f"No replacement was performed. old_str `{old_str}` did not appear verbatim in {path}"
                
                new_content = content.replace(old_str, new_str or '')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return f"The file {path} has been edited. Here's the result of running `cat -n` on a snippet of {path}:\n{new_content[:500]}"
                
            elif command == 'insert':
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                lines.insert(insert_line or 0, (new_str or '') + '\n')
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                return f"The file {path} has been edited. Inserted line at position {insert_line}"
                
            else:
                return f"Unknown command: {command}"
                
        except Exception as e:
            return f"Error executing {command}: {str(e)}"

__all__ = ['file_editor']
