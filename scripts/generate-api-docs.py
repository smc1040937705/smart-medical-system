#!/usr/bin/env python3
"""
Smart Medical System API Documentation Generator

This script generates API documentation from templates and validates the content.
It supports automatic documentation generation, validation, and error reporting.
"""

import os
import json
import yaml
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class APIDocumentationGenerator:
    """API Documentation Generator for Smart Medical System"""
    
    def __init__(self, template_dir: str = "docs/templates", output_dir: str = "docs/api"):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.validation_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "errors": [],
            "warnings": [],
            "files_generated": []
        }
        
    def validate_template_structure(self, template_content: str) -> Dict[str, Any]:
        """Validate the API documentation template structure"""
        validation_result = {
            "valid": True,
            "errors": [],
            "sections_found": []
        }
        
        required_sections = [
            "Overview",
            "Authentication", 
            "Endpoints",
            "Request/Response Examples",
            "Error Codes"
        ]
        
        # Check for required sections
        for section in required_sections:
            if f"## {section}" in template_content:
                validation_result["sections_found"].append(section)
            else:
                validation_result["errors"].append(f"Missing required section: {section}")
                validation_result["valid"] = False
        
        # Check for code examples
        if "```http" not in template_content and "```json" not in template_content:
            validation_result["warnings"].append("No HTTP or JSON code examples found")
        
        # Check for endpoint definitions
        if "GET /" not in template_content and "POST /" not in template_content:
            validation_result["warnings"].append("No HTTP method definitions found")
        
        return validation_result
    
    def generate_api_documentation(self, template_file: str = "api-docs-template.md") -> bool:
        """Generate API documentation from template"""
        try:
            # Read template file
            template_path = self.template_dir / template_file
            if not template_path.exists():
                self.validation_report["errors"].append(f"Template file not found: {template_path}")
                return False
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Validate template structure
            validation = self.validate_template_structure(template_content)
            
            if not validation["valid"]:
                self.validation_report["errors"].extend(validation["errors"])
                self.validation_report["status"] = "failed"
                return False
            
            # Create output directory if it doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate main API documentation
            output_file = self.output_dir / "endpoints.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            self.validation_report["files_generated"].append(str(output_file))
            
            # Generate additional documentation files
            self._generate_supporting_docs(template_content)
            
            # Update validation report
            self.validation_report["status"] = "success"
            self.validation_report["warnings"].extend(validation["warnings"])
            self.validation_report["sections_validated"] = validation["sections_found"]
            
            return True
            
        except Exception as e:
            self.validation_report["errors"].append(f"Generation error: {str(e)}")
            self.validation_report["status"] = "failed"
            return False
    
    def _generate_supporting_docs(self, template_content: str):
        """Generate supporting documentation files"""
        
        # Generate error codes documentation
        error_codes_file = self.output_dir / "error-codes.md"
        error_content = self._extract_error_codes(template_content)
        with open(error_codes_file, 'w', encoding='utf-8') as f:
            f.write(error_content)
        self.validation_report["files_generated"].append(str(error_codes_file))
        
        # Generate authentication documentation
        auth_file = self.output_dir / "authentication.md"
        auth_content = self._extract_authentication_info(template_content)
        with open(auth_file, 'w', encoding='utf-8') as f:
            f.write(auth_content)
        self.validation_report["files_generated"].append(str(auth_file))
        
        # Generate API specification
        spec_file = self.output_dir / "api-specification.json"
        spec_content = self._generate_api_specification(template_content)
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(spec_content, f, indent=2)
        self.validation_report["files_generated"].append(str(spec_file))
    
    def _extract_error_codes(self, content: str) -> str:
        """Extract error codes section"""
        error_section = "# Error Codes\n\n"
        
        # Extract HTTP status codes table
        if "### HTTP Status Codes" in content:
            start_idx = content.find("### HTTP Status Codes")
            end_idx = content.find("### Application Error Codes", start_idx)
            if end_idx == -1:
                end_idx = content.find("##", start_idx + 1)
            
            if start_idx != -1 and end_idx != -1:
                error_section += content[start_idx:end_idx].strip() + "\n\n"
        
        # Extract application error codes
        if "### Application Error Codes" in content:
            start_idx = content.find("### Application Error Codes")
            end_idx = content.find("### Rate Limiting", start_idx)
            if end_idx == -1:
                end_idx = content.find("##", start_idx + 1)
            
            if start_idx != -1 and end_idx != -1:
                error_section += content[start_idx:end_idx].strip() + "\n\n"
        
        return error_section
    
    def _extract_authentication_info(self, content: str) -> str:
        """Extract authentication information"""
        auth_section = "# Authentication\n\n"
        
        if "## Authentication" in content:
            start_idx = content.find("## Authentication")
            end_idx = content.find("##", start_idx + 1)
            
            if start_idx != -1 and end_idx != -1:
                auth_section += content[start_idx:end_idx].strip()
        
        return auth_section
    
    def _generate_api_specification(self, content: str) -> Dict[str, Any]:
        """Generate API specification in JSON format"""
        spec = {
            "api_name": "Smart Medical System API",
            "version": "1.0.0",
            "base_url": "https://api.smart-medical-system.com/v1",
            "authentication": "JWT Bearer Token",
            "endpoints": [],
            "error_codes": [],
            "generated_at": datetime.now().isoformat()
        }
        
        # Extract endpoints from template
        lines = content.split('\n')
        current_endpoint = None
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#### ') and ('GET /' in line or 'POST /' in line):
                if current_endpoint:
                    spec["endpoints"].append(current_endpoint)
                
                method_path = line.replace('#### ', '').strip()
                parts = method_path.split(' ')
                if len(parts) >= 2:
                    current_endpoint = {
                        "method": parts[0],
                        "path": parts[1],
                        "description": ' '.join(parts[2:]) if len(parts) > 2 else "",
                        "parameters": [],
                        "examples": []
                    }
            
            elif current_endpoint and line.strip().startswith('```http'):
                # Extract HTTP example
                example_lines = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('```'):
                    example_lines.append(lines[j])
                    j += 1
                
                if example_lines:
                    current_endpoint["examples"].append({
                        "type": "http",
                        "content": '\n'.join(example_lines)
                    })
        
        if current_endpoint:
            spec["endpoints"].append(current_endpoint)
        
        return spec
    
    def save_validation_report(self, report_file: str = "docs/validation-report.json") -> bool:
        """Save validation report to file"""
        try:
            report_path = Path(report_file)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.validation_report, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving validation report: {e}")
            return False
    
    def print_summary(self):
        """Print generation summary"""
        print("\n" + "="*60)
        print("API Documentation Generation Summary")
        print("="*60)
        
        print(f"Status: {self.validation_report['status'].upper()}")
        print(f"Timestamp: {self.validation_report['timestamp']}")
        
        if self.validation_report['files_generated']:
            print(f"\nFiles Generated ({len(self.validation_report['files_generated'])}):")
            for file in self.validation_report['files_generated']:
                print(f"  ✓ {file}")
        
        if self.validation_report['errors']:
            print(f"\nErrors ({len(self.validation_report['errors'])}):")
            for error in self.validation_report['errors']:
                print(f"  ✗ {error}")
        
        if self.validation_report['warnings']:
            print(f"\nWarnings ({len(self.validation_report['warnings'])}):")
            for warning in self.validation_report['warnings']:
                print(f"  ⚠ {warning}")
        
        if 'sections_validated' in self.validation_report:
            print(f"\nSections Validated ({len(self.validation_report['sections_validated'])}):")
            for section in self.validation_report['sections_validated']:
                print(f"  ✓ {section}")
        
        print("="*60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate API Documentation')
    parser.add_argument('--template', default='api-docs-template.md', 
                       help='Template file name')
    parser.add_argument('--template-dir', default='docs/templates',
                       help='Template directory')
    parser.add_argument('--output-dir', default='docs/api',
                       help='Output directory')
    parser.add_argument('--report-file', default='docs/validation-report.json',
                       help='Validation report file')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = APIDocumentationGenerator(
        template_dir=args.template_dir,
        output_dir=args.output_dir
    )
    
    if args.verbose:
        print("Starting API documentation generation...")
        print(f"Template: {args.template}")
        print(f"Template Directory: {args.template_dir}")
        print(f"Output Directory: {args.output_dir}")
    
    # Generate documentation
    success = generator.generate_api_documentation(args.template)
    
    # Save validation report
    generator.save_validation_report(args.report_file)
    
    # Print summary
    generator.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()