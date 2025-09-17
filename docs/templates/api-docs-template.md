# API Documentation Template

## Overview
This document provides comprehensive API documentation for the Smart Medical System.

## Authentication
- API Key authentication
- OAuth 2.0 support
- JWT token validation

## Endpoints

### Patient Management
- `GET /api/patients` - List all patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/{id}` - Get patient by ID
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Medical Records
- `GET /api/records` - List medical records
- `POST /api/records` - Create new record
- `GET /api/records/{id}` - Get record by ID

## Request/Response Examples

### Create Patient
```json
POST /api/patients
{
  "name": "John Doe",
  "age": 30,
  "medicalId": "MED001"
}
```

### Response
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 30,
  "medicalId": "MED001",
  "createdAt": "2025-09-17T10:00:00Z"
}
```

## Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error