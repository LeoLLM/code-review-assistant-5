#!/usr/bin/env python3
"""
Automated code review logic for analyzing Python code and generating review comments
based on predefined templates.
"""

import os
import re
import ast
import importlib.util
from typing import List, Dict, Any, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CodeReviewAnalyzer:
    """Main class for analyzing code and generating review comments"""
    
    def __init__(self, template_dir: str = "review_templates"):
        """
        Initialize the code review analyzer
        
        Args:
            template_dir: Directory containing the review templates
        """
        self.template_dir = template_dir
        self.templates = self._load_templates()
        self.issues = []
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """
        Load review templates from the template directory
        
        Returns:
            Dictionary mapping template names to checklist items
        """
        templates = {}
        
        if not os.path.exists(self.template_dir):
            logger.warning(f"Template directory '{self.template_dir}' not found")
            return templates
        
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.md'):
                template_name = filename[:-3]  # Remove .md extension
                template_path = os.path.join(self.template_dir, filename)
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                # Extract checklist items
                checklist_items = re.findall(r'- \[ \] (.*)', content)
                templates[template_name] = checklist_items
        
        return templates
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Analyze a Python file for code issues
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            List of issues found in the file
        """
        self.issues = []
        
        if not os.path.exists(file_path):
            logger.error(f"File '{file_path}' not found")
            return self.issues
        
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for various issues
        self._check_security_issues(file_path, content)
        self._check_performance_issues(file_path, content)
        self._check_code_quality_issues(file_path, content)
        
        return self.issues
    
    def _add_issue(self, category: str, line: int, message: str, severity: str = "medium"):
        """Add an issue to the list of issues"""
        self.issues.append({
            "category": category,
            "line": line,
            "message": message,
            "severity": severity
        })
    
    def _check_security_issues(self, file_path: str, content: str):
        """Check for security-related issues"""
        # Check for hardcoded credentials
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'(password|api_key|secret|token).*=.*[\'\"][^\'"]+[\'\"]', line, re.IGNORECASE):
                self._add_issue(
                    "security",
                    i,
                    "Hardcoded credentials detected. Use environment variables instead.",
                    "high"
                )
        
        # Check for SQL injection vulnerabilities
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'SELECT.*\+.*str\(', line, re.IGNORECASE):
                self._add_issue(
                    "security",
                    i,
                    "Potential SQL injection vulnerability. Use parameterized queries.",
                    "high"
                )
        
        # Check for bare except clauses
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'except\s*:', line):
                self._add_issue(
                    "security",
                    i,
                    "Bare except clause found. Specify exceptions to catch.",
                    "medium"
                )
    
    def _check_performance_issues(self, file_path: str, content: str):
        """Check for performance-related issues"""
        # Check for nested loops
        try:
            tree = ast.parse(content)
            
            class NestedLoopVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.loop_depth = 0
                    self.nested_loops = []
                
                def visit_For(self, node):
                    self.loop_depth += 1
                    if self.loop_depth > 1:
                        self.nested_loops.append((node.lineno, self.loop_depth))
                    self.generic_visit(node)
                    self.loop_depth -= 1
                
                def visit_While(self, node):
                    self.loop_depth += 1
                    if self.loop_depth > 1:
                        self.nested_loops.append((node.lineno, self.loop_depth))
                    self.generic_visit(node)
                    self.loop_depth -= 1
            
            visitor = NestedLoopVisitor()
            visitor.visit(tree)
            
            for line, depth in visitor.nested_loops:
                self._add_issue(
                    "performance",
                    line,
                    f"Nested loop (depth {depth}) detected. Consider optimizing.",
                    "medium"
                )
        except SyntaxError:
            logger.warning(f"Could not parse {file_path} for AST analysis")
        
        # Check for resource leaks
        resource_patterns = [
            (r'open\(.*\)', r'close\(\)', "File handle may not be closed properly. Use 'with' statement."),
            (r'connect\(.*\)', r'close\(\)', "Database connection may not be closed properly.")
        ]
        
        for open_pattern, close_pattern, message in resource_patterns:
            if re.search(open_pattern, content) and not re.search(close_pattern, content):
                self._add_issue(
                    "performance",
                    0,  # Line number unknown
                    message,
                    "medium"
                )
    
    def _check_code_quality_issues(self, file_path: str, content: str):
        """Check for code quality issues"""
        # Check for commented out code
        commented_code_pattern = r'^\s*#\s*def\s+|^\s*#\s*class\s+'
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(commented_code_pattern, line):
                self._add_issue(
                    "code_quality",
                    i,
                    "Commented out code found. Remove if not needed.",
                    "low"
                )
        
        # Check for print statements used for debugging
        for i, line in enumerate(content.split('\n'), 1):
            if "print(" in line and not line.strip().startswith("#"):
                context = line.strip()
                if "debug" in context.lower() or "log" not in context.lower():
                    self._add_issue(
                        "code_quality",
                        i,
                        "Debug print statement found. Consider using proper logging.",
                        "low"
                    )
        
        # Check for long functions
        try:
            tree = ast.parse(content)
            
            class FunctionLengthVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.functions = []
                
                def visit_FunctionDef(self, node):
                    end_line = max(getattr(child, 'lineno', node.lineno) for child in ast.walk(node))
                    length = end_line - node.lineno
                    if length > 20:  # Functions longer than 20 lines
                        self.functions.append((node.name, node.lineno, length))
                    self.generic_visit(node)
            
            visitor = FunctionLengthVisitor()
            visitor.visit(tree)
            
            for name, line, length in visitor.functions:
                self._add_issue(
                    "code_quality",
                    line,
                    f"Function '{name}' is {length} lines long. Consider breaking it down.",
                    "medium"
                )
        except SyntaxError:
            logger.warning(f"Could not parse {file_path} for AST analysis")

    def generate_review(self, file_path: str, template_type: str = "general") -> str:
        """
        Generate a code review for a file based on a specific template
        
        Args:
            file_path: Path to the Python file to analyze
            template_type: Type of template to use (general, security, performance)
            
        Returns:
            Review comments as a formatted string
        """
        issues = self.analyze_file(file_path)
        
        # Filter issues based on template type
        relevant_issues = [issue for issue in issues if issue["category"] in template_type]
        
        # Generate review
        review = f"# Code Review for {os.path.basename(file_path)}\n\n"
        review += f"Using the {template_type} template.\n\n"
        
        if not relevant_issues:
            review += "No issues found based on the selected template.\n"
        else:
            review += "## Issues Found\n\n"
            for issue in relevant_issues:
                line_info = f"Line {issue['line']}: " if issue['line'] > 0 else ""
                severity = issue['severity'].upper()
                review += f"- **[{severity}]** {line_info}{issue['message']}\n"
        
        return review

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated code review tool")
    parser.add_argument("file", help="Python file to review")
    parser.add_argument("--template", "-t", default="general", 
                        choices=["general", "security", "performance"],
                        help="Review template to use")
    
    args = parser.parse_args()
    
    analyzer = CodeReviewAnalyzer()
    review = analyzer.generate_review(args.file, args.template)
    
    print(review)

if __name__ == "__main__":
    main()