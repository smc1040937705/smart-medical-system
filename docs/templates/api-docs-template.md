# Smart Medical System API Documentation Template

## Overview

The Smart Medical System API provides a comprehensive set of endpoints for managing medical data, patient records, healthcare providers, and medical appointments. This API follows RESTful principles and uses JSON for data exchange.

### Base URL
```
https://api.smart-medical-system.com/v1
```

### Version
- Current Version: v1.0.0
- API Status: Production Ready

## Authentication

All API requests require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header.

### Authentication Header
```http
Authorization: Bearer <your_jwt_token>
```

### Obtaining a Token
```http
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

## Endpoints

### Patient Management

#### Get All Patients
```http
GET /patients
```

**Response:**
```json
{
  "patients": [
    {
      "id": "patient_123",
      "name": "John Doe",
      "age": 45,
      "gender": "male",
      "medical_history": ["hypertension", "diabetes"],
      "created_at": "2024-01-15T10:30:00Z"
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
Content-Type: application/json

{
  "name": "Jane Smith",
  "age": 32,
  "gender": "female",
  "contact_info": {
    "email": "jane.smith@email.com",
    "phone": "+1234567890"
  },
  "emergency_contact": {
    "name": "John Smith",
    "relationship": "spouse",
    "phone": "+1234567891"
  }
}
```

### Medical Records

#### Get Patient Medical Records
```http
GET /patients/{patient_id}/records
```

**Parameters:**
- `patient_id` (string, required): Unique identifier for the patient

**Response:**
```json
{
  "records": [
    {
      "id": "record_456",
      "patient_id": "patient_123",
      "doctor_id": "doctor_789",
      "visit_date": "2024-01-20T14:30:00Z",
      "diagnosis": "Hypertension",
      "treatment": "Prescribed medication and lifestyle changes",
      "medications": [
        {
          "name": "Lisinopril",
          "dosage": "10mg",
          "frequency": "Once daily"
        }
      ],
      "lab_results": [
        {
          "test_name": "Blood Pressure",
          "result": "140/90 mmHg",
          "normal_range": "<120/80 mmHg"
        }
      ]
    }
  ]
}
```

### Appointment Management

#### Schedule Appointment
```http
POST /appointments
Content-Type: application/json

{
  "patient_id": "patient_123",
  "doctor_id": "doctor_789",
  "appointment_date": "2024-02-01T10:00:00Z",
  "reason": "Regular checkup",
  "duration_minutes": 30
}
```

#### Get Available Time Slots
```http
GET /doctors/{doctor_id}/availability?date=2024-02-01
```

## Request/Response Examples

### Successful Response Format
```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-25T08:30:00Z"
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  },
  "timestamp": "2024-01-25T08:30:00Z"
}
```

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

### Application Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| AUTH_REQUIRED | Authentication required | 401 |
| INVALID_TOKEN | Invalid or expired token | 401 |
| PERMISSION_DENIED | Insufficient permissions | 403 |
| PATIENT_NOT_FOUND | Patient not found | 404 |
| DOCTOR_NOT_FOUND | Doctor not found | 404 |
| APPOINTMENT_CONFLICT | Appointment time conflict | 409 |
| VALIDATION_ERROR | Input validation failed | 422 |
| DATABASE_ERROR | Database operation failed | 500 |

### Rate Limiting

- Maximum requests: 1000 per hour per API key
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets

## Data Models

### Patient Model
```json
{
  "id": "string",
  "name": "string",
  "age": "number",
  "gender": "string",
  "contact_info": {
    "email": "string",
    "phone": "string",
    "address": "string"
  },
  "emergency_contact": {
    "name": "string",
    "relationship": "string",
    "phone": "string"
  },
  "medical_history": "array",
  "allergies": "array",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Doctor Model
```json
{
  "id": "string",
  "name": "string",
  "specialization": "string",
  "license_number": "string",
  "contact_info": {
    "email": "string",
    "phone": "string",
    "office_address": "string"
  },
  "availability": "array",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Testing

### Test Environment
- Base URL: `https://test-api.smart-medical-system.com/v1`
- Test data is reset daily
- No rate limiting in test environment

### Sample Test Credentials
```json
{
  "username": "test_user",
  "password": "test_password_123"
}
```

## Support

For API support and questions:
- Email: api-support@smart-medical-system.com
- Documentation: https://docs.smart-medical-system.com
- Status Page: https://status.smart-medical-system.com