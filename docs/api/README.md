# Smart Medical System API Documentation

This directory contains automatically generated API documentation for the Smart Medical System.

## Overview

The API documentation system automatically generates comprehensive documentation from templates, validates the content, and provides detailed reports on the generation process.

## Generated Files

### Main Documentation
- **`endpoints.md`** - Complete API documentation with all endpoints, examples, and usage instructions
- **`error-codes.md`** - Detailed error code reference
- **`authentication.md`** - Authentication methods and examples
- **`api-specification.json`** - Machine-readable API specification

### Supporting Files
- **`validation-report.json`** - Validation results and generation statistics

## Usage

### Manual Generation
To generate documentation manually:

```bash
# Generate all documentation
python scripts/generate-api-docs.py

# Generate with verbose output
python scripts/generate-api-docs.py --verbose

# Generate with custom template
python scripts/generate-api-docs.py --template custom-template.md
```

### Automated Generation
Documentation is automatically generated:
- On push to `main` or `develop` branches
- On pull requests to `main` branch
- When template files are modified
- Manually via GitHub Actions workflow dispatch

## Template Structure

API documentation templates should include the following sections:

1. **Overview** - API introduction and base information
2. **Authentication** - Authentication methods and examples
3. **Endpoints** - All API endpoints with HTTP methods
4. **Request/Response Examples** - Code examples for each endpoint
5. **Error Codes** - HTTP status codes and application error codes

## Validation

The documentation generation process includes comprehensive validation:

- **Template Validation** - Ensures all required sections are present
- **Content Validation** - Checks for code examples and proper formatting
- **File Validation** - Verifies generated files are properly created
- **Quality Checks** - Validates file sizes and JSON structure

## Workflow

The automated workflow includes:

1. **Documentation Generation** - Creates documentation from templates
2. **Validation** - Validates generated content
3. **Quality Checks** - Runs additional quality assessments
4. **Artifact Upload** - Makes documentation available as artifacts
5. **Reporting** - Provides detailed generation reports

## Customization

### Adding New Endpoints
To add new endpoints, update the template file:

1. Edit `docs/templates/api-docs-template.md`
2. Add the new endpoint following the existing format
3. Include request/response examples
4. The system will automatically generate updated documentation

### Custom Templates
Create custom templates by:

1. Adding new template files to `docs/templates/`
2. Using the `--template` parameter with the generator
3. Ensuring templates follow the required structure

## Support

For issues with API documentation generation:

- Check the validation report: `docs/validation-report.json`
- Review GitHub Actions workflow logs
- Verify template structure meets requirements
- Ensure all required sections are included

## Version History

- **v1.0.0** - Initial automated documentation system
- Includes template-based generation
- Comprehensive validation and reporting
- GitHub Actions integration
- Quality assurance checks