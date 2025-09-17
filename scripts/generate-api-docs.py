#!/usr/bin/env python3
"""
Smart Medical System API Documentation Generator

This script generates API documentation from templates and validates the format.
It supports automatic documentation generation and validation for CI/CD pipelines.
"""

import os
import sys
import json
import argparse
import datetime
from typing import Dict, List, Any, Optional


def validate_template_structure(template_path: str) -> Dict[str, bool]:
    """Validate that the API documentation template contains all required sections."""
    validation_results = {
        'has_overview': False,
        'has_authentication': False,
        'has_endpoints': False,
        'has_examples': False,
        'has_error_codes': False,
        'is_valid_markdown': False
    }
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required sections
        validation_results['has_overview'] = '## Overview' in content
        validation_results['has_authentication'] = '## Authentication' in content
        validation_results['has_endpoints'] = '## Endpoints' in content
        validation_results['has_examples'] = '## Request/Response Examples' in content or '## Examples' in content
        validation_results['has_error_codes'] = '## Error Codes' in content
        
        # Basic markdown validation
        validation_results['is_valid_markdown'] = (
            '# ' in content and  # Has at least one header
            '```' in content     # Has code blocks
        )
        
        return validation_results
        
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        return {key: False for key in validation_results}
    except Exception as e:
        print(f"Error reading template: {e}")
        return {key: False for key in validation_results}


def generate_api_docs(template_path: str, output_path: str, variables: Optional[Dict] = None) -> bool:
    """Generate API documentation from template with variable substitution."""
    if variables is None:
        variables = {}
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Add default variables
        default_vars = {
            'generation_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0.0',
            'base_url': 'https://api.smart-medical-system.com/v1'
        }
        variables = {**default_vars, **variables}
        
        # Simple variable substitution
        for key, value in variables.items():
            template_content = template_content.replace(f'{{{{{key}}}}}', str(value))
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✓ API documentation generated successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error generating API documentation: {e")
        return False


def validate_generated_docs(docs_path: str) -> Dict[str, Any]:
    """Validate the generated API documentation."""
    validation_report = {
        'valid': False,
        'errors': [],
        'warnings': [],
        'stats': {}
    }
    
    try:
        with open(docs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic validation checks
        checks = [
            ('has_main_header', '# ' in content and content.startswith('#')),
            ('has_code_blocks', '```' in content),
            ('has_http_examples', '```http' in content or 'HTTP/' in content),
            ('has_json_examples', '```json' in content),
            ('has_endpoint_definitions', any(method in content for method in ['GET ', 'POST ', 'PUT ', 'DELETE ', 'PATCH '])),
        ]
        
        for check_name, check_result in checks:
            validation_report['stats'][check_name] = check_result
            if not check_result:
                validation_report['warnings'].append(f"Missing {check_name.replace('_', ' ')}")
        
        # Count sections
        sections = content.count('## ')
        validation_report['stats']['section_count'] = sections
        
        if sections >= 5:  # At least Overview, Auth, Endpoints, Examples, Error Codes
            validation_report['valid'] = True
        else:
            validation_report['errors'].append(f"Insufficient sections: {sections} found, need at least 5")
        
        return validation_report
        
    except Exception as e:
        validation_report['errors'].append(f"Validation error: {e}")
        return validation_report


def create_validation_report(validation_results: Dict[str, Any], output_path: str) -> bool:
    """Create a validation report in JSON format."""
    try:
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'validation_results': validation_results,
            'summary': {
                'is_valid': validation_results['valid'],
                'error_count': len(validation_results['errors']),
                'warning_count': len(validation_results['warnings'])
            }
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Validation report generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating validation report: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate and validate API documentation')
    parser.add_argument('--template', '-t', default='docs/api-docs-template.md', 
                       help='Path to API documentation template')
    parser.add_argument('--output', '-o', default='docs/api/endpoints.md', 
                       help='Output path for generated documentation')
    parser.add_argument('--validate-only', action='store_true', 
                       help='Only validate existing documentation without generating')
    parser.add_argument('--report', '-r', default='docs/validation-report.json', 
                       help='Path for validation report')
    parser.add_argument('--variables', '-v', type=json.loads, default='{}',
                       help='JSON string of template variables')
    
    args = parser.parse_args()
    
    print("🔧 Smart Medical System API Documentation Generator")
    print("=" * 60)
    
    if not args.validate_only:
        # Generate documentation
        print(f"📄 Generating documentation from template: {args.template}")
        success = generate_api_docs(args.template, args.output, args.variables)
        if not success:
            sys.exit(1)
    
    # Validate template structure
    print(f"\n✅ Validating template structure: {args.template}")
    template_validation = validate_template_structure(args.template)
    
    if not all(template_validation.values()):
        print("⚠️  Template validation issues:")
        for key, valid in template_validation.items():
            status = "✓" if valid else "✗"
            print(f"  {status} {key}: {valid}")
    else:
        print("✓ Template structure validation passed")
    
    # Validate generated documentation
    print(f"\n🔍 Validating generated documentation: {args.output}")
    docs_validation = validate_generated_docs(args.output)
    
    if docs_validation['valid']:
        print("✓ Generated documentation validation passed")
    else:
        print("✗ Generated documentation validation failed:")
        for error in docs_validation['errors']:
            print(f"  • {error}")
    
    if docs_validation['warnings']:
        print("⚠️  Warnings:")
        for warning in docs_validation['warnings']:
            print(f"  • {warning}")
    
    # Create validation report
    print(f"\n📊 Generating validation report: {args.report}")
    full_validation_results = {
        'template_validation': template_validation,
        'docs_validation': docs_validation,
        'overall_valid': template_validation and docs_validation['valid']
    }
    
    report_success = create_validation_report(full_validation_results, args.report)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 Validation Summary:")
    print(f"  Template Valid: {all(template_validation.values())}")
    print(f"  Docs Valid: {docs_validation['valid']}")
    print(f"  Errors: {len(docs_validation['errors'])}")
    print(f"  Warnings: {len(docs_validation['warnings'])}")
    
    if not (all(template_validation.values()) and docs_validation['valid']):
        print("\n❌ Validation failed!")
        sys.exit(1)
    else:
        print("\n🎉 All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()