# Smart Medical System API Documentation

## Overview

The Smart Medical System API provides a comprehensive set of endpoints for managing medical data, patient records, appointments, and healthcare operations. This RESTful API follows standard HTTP conventions and returns JSON responses.

**Base URL**: `https://api.smart-medical-system.com/v1`

## Authentication

All API requests require authentication using Bearer tokens. Include the token in the Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Obtaining an Access Token

1. Register your application to get client credentials
2. Use the OAuth 2.0 authorization flow
3. Exchange authorization code for access token

## Endpoints

### Patients

#### Get All Patients
```http
GET /patients
```

**Response**: Array of patient objects

#### Get Patient by ID
```http
GET /patients/{id}
```

**Parameters**:
- `id` (path) - Patient identifier

#### Create Patient
```http
POST /patients
```

**Request Body**: Patient creation data

### Appointments

#### Get All Appointments
```http
GET /appointments
```

**Query Parameters**:
- `date` (optional) - Filter by date
- `status` (optional) - Filter by status

#### Create Appointment
```http
POST /appointments
```

**Request Body**: Appointment creation data

### Medical Records

#### Get Patient Medical Records
```http
GET /patients/{id}/records
```

#### Add Medical Record
```http
POST /patients/{id}/records
```

### Healthcare Providers

#### Get All Providers
```http
GET /providers
```

#### Get Provider by ID
```http
GET /providers/{id}
```

## Request/Response Examples

### Example: Get Patient by ID

**Request**:
```http
GET /patients/12345
Authorization: Bearer abc123def456
```

**Response**:
```json
{
  "id": 12345,
  "name": "John Doe",
  "dateOfBirth": "1985-03-15",
  "gender": "male",
  "contact": {
    "email": "john.doe@example.com",
    "phone": "+1-555-0123"
  },
  "medicalHistory": [
    {
      "condition": "Hypertension",
      "diagnosisDate": "2020-01-15",
      "status": "managed"
    }
  ],
  "createdAt": "2023-01-15T10:30:00Z",
  "updatedAt": "2023-12-01T14:25:00Z"
}
```

### Example: Create Appointment

**Request**:
```http
POST /appointments
Authorization: Bearer abc123def456
Content-Type: application/json

{
  "patientId": 12345,
  "providerId": 67890,
  "appointmentDate": "2024-01-20T14:00:00Z",
  "reason": "Routine checkup",
  "duration": 30
}
```

**Response**:
```json
{
  "id": 98765,
  "patientId": 12345,
  "providerId": 67890,
  "appointmentDate": "2024-01-20T14:00:00Z",
  "reason": "Routine checkup",
  "duration": 30,
  "status": "scheduled",
  "createdAt": "2024-01-15T09:45:00Z"
}
```

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Authentication required or invalid |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server-side issue |

### Error Response Format

```json
{
  "error": {
    "code": "invalid_input",
    "message": "Invalid input parameters provided",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Common Error Codes

- `invalid_token` - Access token is invalid or expired
- `insufficient_permissions` - User lacks required permissions
- `resource_not_found` - Requested resource does not exist
- `validation_error` - Input validation failed
- `rate_limit_exceeded` - Too many requests in given timeframe

## Rate Limiting

- **Standard**: 1000 requests per hour
- **Burst**: 100 requests per minute
- **Headers**:
  - `X-RateLimit-Limit` - Total requests allowed
  - `X-RateLimit-Remaining` - Requests remaining
  - `X-RateLimit-Reset` - Time when limit resets

## Versioning

API version is specified in the URL path. Current version: `v1`

When breaking changes are introduced, a new version will be released with proper deprecation notices.

## Support

For API support and questions:
- Documentation: https://docs.smart-medical-system.com
- Support Email: api-support@smart-medical-system.com
- Issue Tracker: https://github.com/smc1040937705/smart-medical-system/issues