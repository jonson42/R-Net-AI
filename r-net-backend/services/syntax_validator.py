"""
Syntax validation for generated code files
"""

import ast
import json
import logging
from typing import Dict, List, Tuple
from models import GeneratedFile

logger = logging.getLogger(__name__)


class SyntaxValidator:
    """
    Validates syntax of generated code files before returning to user
    """
    
    @staticmethod
    def validate_python(content: str) -> Tuple[bool, str]:
        """Validate Python syntax"""
        try:
            ast.parse(content)
            return True, "Valid Python syntax"
        except SyntaxError as e:
            return False, f"Python syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Python validation error: {str(e)}"
    
    @staticmethod
    def validate_json(content: str) -> Tuple[bool, str]:
        """Validate JSON syntax"""
        try:
            json.loads(content)
            return True, "Valid JSON syntax"
        except json.JSONDecodeError as e:
            return False, f"JSON syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"JSON validation error: {str(e)}"
    
    @staticmethod
    def validate_javascript(content: str) -> Tuple[bool, str]:
        """
        Basic JavaScript/TypeScript syntax validation
        Checks for common syntax errors without full parsing
        """
        # Check for balanced braces/brackets/parentheses
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        line_num = 1
        
        in_string = False
        string_char = None
        in_comment = False
        
        for i, char in enumerate(content):
            if char == '\n':
                line_num += 1
                in_comment = False  # Single-line comment ends
            
            # Handle comments
            if i < len(content) - 1:
                if content[i:i+2] == '//':
                    in_comment = True
                elif content[i:i+2] == '/*':
                    in_comment = True
                elif content[i:i+2] == '*/':
                    in_comment = False
                    continue
            
            if in_comment:
                continue
            
            # Handle strings
            if char in ['"', "'", '`'] and (i == 0 or content[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            if in_string:
                continue
            
            # Check brackets
            if char in pairs:
                stack.append((char, line_num))
            elif char in pairs.values():
                if not stack:
                    return False, f"Unmatched closing '{char}' at line {line_num}"
                open_char, open_line = stack.pop()
                if pairs[open_char] != char:
                    return False, f"Mismatched brackets: '{open_char}' at line {open_line} closed with '{char}' at line {line_num}"
        
        if stack:
            unclosed = stack[-1]
            return False, f"Unclosed '{unclosed[0]}' at line {unclosed[1]}"
        
        # Basic checks for common errors
        if 'function(' in content or 'function (' in content:
            # Check for arrow functions without proper syntax
            pass
        
        return True, "Valid JavaScript/TypeScript syntax (basic check)"
    
    @staticmethod
    def validate_html(content: str) -> Tuple[bool, str]:
        """Validate HTML syntax (basic tag matching)"""
        from html.parser import HTMLParser
        
        class HTMLValidator(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack = []
                self.errors = []
            
            def handle_starttag(self, tag, attrs):
                # Self-closing tags
                if tag in ['img', 'br', 'hr', 'input', 'meta', 'link']:
                    return
                self.stack.append(tag)
            
            def handle_endtag(self, tag):
                if not self.stack:
                    self.errors.append(f"Unexpected closing tag: </{tag}>")
                    return
                
                if self.stack and self.stack[-1] == tag:
                    self.stack.pop()
                else:
                    self.errors.append(f"Mismatched tag: expected </{self.stack[-1]}>, got </{tag}>")
        
        try:
            validator = HTMLValidator()
            validator.feed(content)
            
            if validator.errors:
                return False, f"HTML errors: {', '.join(validator.errors[:3])}"
            
            if validator.stack:
                return False, f"Unclosed tags: {', '.join(validator.stack[:3])}"
            
            return True, "Valid HTML syntax"
        except Exception as e:
            return False, f"HTML validation error: {str(e)}"
    
    @staticmethod
    def validate_css(content: str) -> Tuple[bool, str]:
        """Validate CSS syntax (basic check)"""
        # Check for balanced braces
        brace_count = content.count('{') - content.count('}')
        if brace_count != 0:
            return False, f"CSS syntax error: Unbalanced braces ({brace_count} unclosed)"
        
        # Check for basic CSS structure
        lines = content.split('\n')
        in_rule = False
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('/*') or line.startswith('//'):
                continue
            
            if '{' in line:
                in_rule = True
            
            if in_rule and ':' in line and ';' not in line and '}' not in line:
                # CSS property without semicolon (warning, not error)
                pass
            
            if '}' in line:
                in_rule = False
        
        return True, "Valid CSS syntax (basic check)"
    
    @staticmethod
    def get_validator_for_file(file_path: str):
        """Get appropriate validator based on file extension"""
        file_path_lower = file_path.lower()
        
        if file_path_lower.endswith('.py'):
            return SyntaxValidator.validate_python
        elif file_path_lower.endswith('.json'):
            return SyntaxValidator.validate_json
        elif file_path_lower.endswith(('.js', '.jsx', '.ts', '.tsx')):
            return SyntaxValidator.validate_javascript
        elif file_path_lower.endswith(('.html', '.htm')):
            return SyntaxValidator.validate_html
        elif file_path_lower.endswith('.css'):
            return SyntaxValidator.validate_css
        else:
            return None  # No validator for this file type
    
    @staticmethod
    def validate_files(files: List[GeneratedFile]) -> Dict:
        """
        Validate all generated files and return validation report
        
        Returns:
            {
                "valid": bool,
                "total_files": int,
                "validated_files": int,
                "errors": [{"file": str, "error": str}, ...],
                "warnings": [str, ...]
            }
        """
        total_files = len(files)
        validated_count = 0
        errors = []
        warnings = []
        
        logger.info(f"Validating syntax for {total_files} generated files")
        
        for file in files:
            validator = SyntaxValidator.get_validator_for_file(file.path)
            
            if validator is None:
                # No validator for this file type (e.g., .md, .txt, .env)
                warnings.append(f"No validator available for {file.path}")
                continue
            
            validated_count += 1
            is_valid, message = validator(file.content)
            
            if not is_valid:
                logger.error(f"Syntax error in {file.path}: {message}")
                errors.append({
                    "file": file.path,
                    "error": message
                })
            else:
                logger.debug(f"✓ {file.path}: {message}")
        
        is_all_valid = len(errors) == 0
        
        result = {
            "valid": is_all_valid,
            "total_files": total_files,
            "validated_files": validated_count,
            "errors": errors,
            "warnings": warnings
        }
        
        if is_all_valid:
            logger.info(f"✓ All {validated_count} files passed syntax validation")
        else:
            logger.warning(f"✗ {len(errors)} files have syntax errors out of {validated_count} validated")
        
        return result
    
    @staticmethod
    def create_fix_prompt(file_path: str, content: str, error_message: str) -> str:
        """
        Create a prompt to ask AI to fix syntax errors
        """
        return f"""The following file has a syntax error:

File: {file_path}
Error: {error_message}

Please fix the syntax error and return ONLY the corrected file content.
Ensure the code is syntactically correct and follows best practices.

Current content:
```
{content}
```

Return the fixed code:"""


# Global validator instance
syntax_validator = SyntaxValidator()
