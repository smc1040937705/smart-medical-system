# Smart Medical System API Documentation

## Overview

The Smart Medical System API provides a comprehensive set of endpoints for managing medical data, patient records, appointments, and healthcare operations. This API follows RESTful principles and uses JSON for data exchange.

**Base URL**: `https://api.smart-medical-system.com/v1`
**Content-Type**: `application/json`

## Authentication

All API requests require authentication using Bearer tokens. Include the token in the Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Obtaining Access Tokens

1. **Login Endpoint**: `POST /auth/login`
2. **Token Refresh**: `POST /auth/refresh`
3. **Token Validation**: `GET /auth/validate`

Tokens expire after 24 hours and must be refreshed.

## Endpoints

### Patients Management

#### Get All Patients
```http
GET /patients
```

**Response**:
```json
{
  "patients": [
    {
      "id": "pat_123",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
  "date_of_birth": "1985-03-15",
  "gender": "male",
      "medical_history": [],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_count": 1,
  "page": 1,
  "per_page": 20
}
```

#### Create Patient
```http
POST /patients
```

**Request Body**:
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "+0987654321",
  "date_of_birth": "1990-08-22",
  "gender": "female",
  "address": "123 Medical St, Healthcare City"
}
```

### Appointments

#### Schedule Appointment
```http
POST /appointments
```

**Request Body**:
```json
{
  "patient_id": "pat_123",
  "doctor_id": "doc_456",
  "scheduled_time": "2024-01-20T14:30:00Z",
  "duration_minutes": 30,
  "reason": "Routine checkup",
  "notes": "Patient has allergy to penicillin"
}
```

#### Get Appointment by ID
```http
GET /appointments/{appointment_id}
```

### Medical Records

#### Upload Medical Record
```http
POST /medical-records
Content-Type: multipart/form-data
```

**Form Data**:
- `file`: Medical document (PDF, JPG, PNG)
- `patient_id`: Patient identifier
- `record_type`: Type of record (lab_result, prescription, xray, etc.)
- `description`: Brief description

#### Get Patient Medical Records
```http
GET /patients/{patient_id}/medical-records
```

## Request/Response Examples

### Example: Creating a New Patient

**Request**:
```http
POST /patients
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "Michael Chen",
  "email": "michael.chen@example.com",
  "phone": "+1122334455",
  "date_of_birth": "1988-12-03",
  "gender": "male",
  "address": "456 Health Ave, Wellness City"
}
```

**Response**:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "pat_789",
  "name": "Michael Chen",
  "email": "michael.chen@example.com",
  "phone": "+1122334455",
  "date_of_birth": "1988-12-03",
  "gender": "male",
  "address": "456 Health Ave, Wellness City",
  "created_at": "2024-01-16T09:15:00Z",
  "updated_at": "2024-01-16T09:15:00Z"
}
```

### Example: Error Response

**Request**:
```http
GET /patients/invalid_id
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response**:
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": {
    "code": "PATIENT_NOT_FOUND",
    "message": "Patient with ID 'invalid_id' not found",
    "details": "Please check the patient ID and try again"
  }
}
```

## Error Codes

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server error

### Application Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `AUTH_INVALID_TOKEN` | Invalid or expired authentication token | 401 |
| `AUTH_MISSING_TOKEN` | Authorization header missing | 401 |
| `PATIENT_NOT_FOUND` | Patient record not found | 404 |
| `PATIENT_DUPLICATE_EMAIL` | Email address already registered | 409 |
| `APPOINTMENT_CONFLICT` | Appointment time conflict | 409 |
| `VALIDATION_ERROR` | Request validation failed | 422 |
| `FILE_UPLOAD_ERROR` | File upload failed | 500 |
| `DATABASE_ERROR` | Database operation failed | 500 |

### Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional details or context",
    "timestamp": "2024-01-16T10:30:45Z"
  }
}
```

## Rate Limiting

- **Standard Users**: 100 requests per hour
- **Premium Users**: 1000 requests per hour
- **System Administrators**: 5000 requests per hour

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when limit resets (UTC timestamp)

## Versioning

API version is specified in the URL path (`/v1/`). Breaking changes will result in new version numbers. Non-breaking changes will be backward compatible.

## Support

For API support and questions:
- Email: api-support@smart-medical-system.com
- Documentation: https://docs.smart-medical-system.com
- Status Page: https://status.smart-medical-system.com