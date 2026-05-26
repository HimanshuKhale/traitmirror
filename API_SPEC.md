# API Spec

## Ideal Self
POST /api/traits/ideal-profile/
GET /api/traits/ideal-profile/

## Assessment
GET /api/assessments/questions/next/
POST /api/assessments/answers/
POST /api/assessments/complete/

## Narrative
POST /api/narratives/start/
POST /api/narratives/{id}/answer/
GET /api/narratives/{id}/followups/
POST /api/narratives/{id}/complete/

## Growth
GET /api/growth/daily-plan/
POST /api/growth/practice-event/