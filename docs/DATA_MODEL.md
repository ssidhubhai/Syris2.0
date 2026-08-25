# DATA_MODEL.md — V1 Persistence Model

## Core tables/entities

### users
- id
- preferences
- created_at

### sessions
- id
- user_id
- title
- subject
- current_state
- created_at
- updated_at

### messages
- id
- session_id
- role
- content
- attachments
- created_at

### problems
- id
- session_id
- source_image
- normalized_text
- subject
- metadata

### attempts
- id
- problem_id
- raw_input
- normalized_input
- analysis

### explanation_documents
- id
- session_id
- version
- document_json
- validation_json
- provider_metadata
- created_at

### whiteboard_states
- id
- explanation_document_id
- state_json
- version

### model_requests
- id
- session_id
- provider
- model
- request_type
- latency_ms
- token_usage_if_available
- status
- error_code
- created_at

### mistakes (optional V1-lite)
- id
- session_id
- concept
- category
- evidence
- created_at

## V1 note

Do not implement a giant mastery/FSRS/prerequisite graph unless it is required by the user-facing V1. Store enough structured data now that future systems can be added without redesigning session history.
