<!-- Generated: 2025-09-17 06:48:48 -->

# Smart Medical System API Documentation

## Overview

The Smart Medical System API provides a comprehensive set of endpoints for managing patient records, medical appointments, prescriptions, and healthcare provider information. This RESTful API follows standard HTTP conventions and returns JSON responses.

**Base URL**: `https://api.smart-medical-system.com/v1`

## Authentication

All API requests require authentication using Bearer tokens. Include the token in the Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Obtaining an Access Token

1. Register your application to obtain client credentials
2. Use the OAuth 2.0 authorization flow
3. Exchange the authorization code for an access token

## Endpoints

### Patients

#### Get All Patients
```http
GET /patients
```

**Response**: List of patient objects

#### Get Patient by ID
```http
GET /patients/{id}
```

**Parameters**:
- `id` (string, required): Patient identifier

#### Create Patient
```http
POST /patients
```

**Request Body**: Patient creation object

#### Update Patient
```http
PUT /patients/{id}
```

**Parameters**:
- `id` (string, required): Patient identifier

### Appointments

#### Get All Appointments
```http
GET /appointments
```

**Query Parameters**:
- `date` (string, optional): Filter by date (YYYY-MM-DD)
- `status` (string, optional): Filter by status (scheduled, completed, cancelled)

#### Create Appointment
```http
POST /appointments
```

**Request Body**: Appointment creation object

#### Update Appointment Status
```http
PATCH /appointments/{id}/status
```

**Parameters**:
- `id` (string, required): Appointment identifier

### Prescriptions

#### Get Patient Prescriptions
```http
GET /patients/{patientId}/prescriptions
```

**Parameters**:
- `patientId` (string, required): Patient identifier

#### Create Prescription
```http
POST /prescriptions
```

**Request Body**: Prescription creation object

### Healthcare Providers

#### Get All Providers
```http
GET /providers
```

**Query Parameters**:
- `specialty` (string, optional): Filter by medical specialty
- `availability` (boolean, optional): Filter by availability status

#### Get Provider by ID
```http
GET /providers/{id}
```

**Parameters**:
- `id` (string, required): Provider identifier

## Request/Response Examples

### Example: Create Patient

**Request**:
```http
POST /patients
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1985-03-15",
  "gender": "male",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zipCode": "12345"
  },
  "emergencyContact": {
    "name": "Jane Doe",
    "relationship": "spouse",
    "phone": "+1987654321"
  }
}
```

**Response**:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "pat_1234567890",
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1985-03-15",
  "gender": "male",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zipCode": "12345"
  },
  "emergencyContact": {
    "name": "Jane Doe",
    "relationship": "spouse",
    "phone": "+1987654321"
  },
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### Example: Get Appointment

**Request**:
```http
GET /appointments/apt_9876543210
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "apt_9876543210",
  "patientId": "pat_1234567890",
  "providerId": "prov_555666777",
  "scheduledTime": "2024-01-20T14:30:00Z",
  "duration": 30,
  "status": "scheduled",
  "reason": "Annual checkup",
  "notes": "Patient has concerns about blood pressure",
  "createdAt": "2024-01-15T11:45:00Z",
  "updatedAt": "2024-01-15T11:45:00Z"
}
```

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Authentication required or invalid |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation errors |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server-side error |
| 503 | Service Unavailable - Service temporarily unavailable |

### Error Response Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request contains invalid parameters",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
  "requestId": "req_1234567890",
  "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

### Common Error Codes

| Error Code | Description | HTTP Status |
|------------|-------------|-------------|
| `invalid_token` | Access token is invalid or expired | 401 |
| `insufficient_scope` | Token lacks required permissions | 403 |
| `resource_not_found` | Requested resource does not exist | 404 |
| `validation_error` | Request data validation failed | 422 |
| `rate_limit_exceeded` | Too many requests in time period | 429 |
| `internal_error` | Unexpected server error | 500 |

## Rate Limiting

- **Standard Tier**: 1000 requests per hour
- **Premium Tier**: 5000 requests per hour
- **Enterprise Tier**: Custom limits

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets (UTC timestamp)

## Versioning

The API is versioned through the URL path. The current version is `v1`.

Example: `https://api.smart-medical-system.com/v1/patients`

## Support

For API support and questions:
- Email: api-support@smart-medical-system.com
- Documentation: https://docs.smart-medical-system.com
- Status Page: https://status.smart-medical-system.com

## Changelog

### v1.0.0 (2024-01-15)
- Initial release of Smart Medical System API
- Patient management endpoints
- Appointment scheduling system
- Prescription management
- Healthcare provider directory