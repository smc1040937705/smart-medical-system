#!/usr/bin/env python3
"""
Smart Medical System API Documentation Generator

This script generates API documentation from templates and validates the content.
It supports automatic documentation generation and validation for the Smart Medical System.
"""

import os
import json
import re
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_template(template_path: str) -> str:
    """Load the API documentation template file."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)


def validate_template_content(content: str) -> Dict[str, Any]:
    """Validate that the template contains all required sections."""
    validation_results = {
        'has_overview': False,
        'has_authentication': False,
        'has_endpoints': False,
        'has_examples': False,
        'has_error_codes': False,
        'sections_found': [],
        'issues': []
    }
    
    # Check for required sections
    sections_to_check = [
        ('Overview', 'has_overview'),
        ('Authentication', 'has_authentication'),
        ('Endpoints', 'has_endpoints'),
        ('Request/Response Examples', 'has_examples'),
        ('Error Codes', 'has_error_codes')
    ]
    
    for section_name, flag_name in sections_to_check:
        pattern = rf'^#+\s+{section_name}'  # Match headers like ## Overview
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            validation_results[flag_name] = True
            validation_results['sections_found'].append(section_name)
        else:
            validation_results['issues'].append(f"Missing section: {section_name}")
    
    # Check for code examples
    code_blocks = re.findall(r'```(?:http|json|javascript|python)', content, re.IGNORECASE)
    if not code_blocks:
        validation_results['issues'].append("No code examples found")
    
    # Check for HTTP methods
    http_methods = re.findall(r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b', content)
    if not http_methods:
        validation_results['issues'].append("No HTTP methods found in endpoints")
    
    return validation_results


def generate_api_docs(template_content: str, output_path: str) -> str:
    """Generate final API documentation from template."""
    # Add generation timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    generated_content = f"<!-- Generated: {timestamp} -->\n\n{template_content}"
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_content)
        
        return f"Documentation generated successfully at {output_path}"
    except Exception as e:
        return f"Error generating documentation: {e}"


def create_validation_report(validation_results: Dict[str, Any], report_path: str) -> None:
    """Create a validation report in JSON format."""
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'validation_results': validation_results,
        'is_valid': len(validation_results['issues']) == 0,
        'summary': {
            'total_sections_found': len(validation_results['sections_found']),
            'total_issues': len(validation_results['issues']),
            'required_sections_present': all([
                validation_results['has_overview'],
                validation_results['has_authentication'],
                validation_results['has_endpoints'],
                validation_results['has_examples'],
                validation_results['has_error_codes']
            ])
        }
    }
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error creating validation report: {e}")


def main():
    """Main function to handle command line arguments and execute the script."""
    parser = argparse.ArgumentParser(description='Generate API documentation from template')
    parser.add_argument('--template', '-t', default='docs/templates/api-docs-template.md',
                       help='Path to template file')
    parser.add_argument('--output', '-o', default='docs/api/endpoints.md',
                       help='Output path for generated documentation')
    parser.add_argument('--report', '-r', default='docs/validation-report.json',
                       help='Path for validation report')
    parser.add_argument('--validate-only', '-v', action='store_true',
                       help='Only validate template without generating output')
    
    args = parser.parse_args()
    
    print("🔍 Smart Medical System API Documentation Generator")
    print("=" * 60)
    
    # Load template
    print(f"📄 Loading template from: {args.template}")
    template_content = load_template(args.template)
    
    # Validate template
    print("✅ Validating template content...")
    validation_results = validate_template_content(template_content)
    
    # Create validation report
    create_validation_report(validation_results, args.report)
    
    # Display validation results
    print(f"\n📊 Validation Results:")
    print(f"   • Required sections found: {len(validation_results['sections_found'])}/5")
    print(f"   • Issues detected: {len(validation_results['issues'])}")
    
    if validation_results['issues']:
        print(f"\n❌ Issues found:")
        for issue in validation_results['issues']:
            print(f"   - {issue}")
    else:
        print(f"\n✅ All validation checks passed!")
    
    # Generate documentation if validation passed or if forced
    if not args.validate_only:
        if validation_results['issues']:
            print(f"\n⚠️  Issues found. Documentation generation skipped.")
            print("   Use --validate-only to skip generation or fix the template.")
        else:
            print(f"\n🚀 Generating API documentation...")
            result = generate_api_docs(template_content, args.output)
            print(f"   {result}")
    
    print(f"\n📋 Validation report saved to: {args.report}")
    
    # Exit with appropriate code
    if validation_results['issues']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()