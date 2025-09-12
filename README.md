# Worship_Session_Integration

A full-stack cloud-ready audio management platform with **FastAPI backend**, **Celery worker**, **mobile frontend** (React Native / Expo), and **web frontend** (React). Supports uploads to S3/GCP/Azure, background audio processing, playlists, and secure JWT-based authentication.

---

## Features

### Backend
- FastAPI REST API
- JWT authentication with refresh tokens
- Role-based access control
- Upload presign & complete endpoints for cloud storage
- Playlist/session grouping
- Waveform visualization
- Audio metadata extraction
- Rate limiting & input validation
- Dockerized for cloud & local dev
- Celery + Redis background worker for transcoding & metadata

### Frontend
- **Web client**: React + TypeScript, integrates with backend API
- **Mobile client**: React Native / Expo, cross-platform
- Playlist and audio playback support
- Already compatible with existing web/app frontends

### Cloud Storage
- AWS S3, GCP Cloud Storage, Azure Blob Storage
- Direct-to-cloud presigned URL uploads
- Server-side fallback

### DevOps & Deployment
- Dockerfiles for backend & Celery worker
- Docker Compose for local development
- Ready for GKE, AWS ECS, Azure App Service
- HTTPS-ready and secure environment handling

---

## Setup

### 1. Clone the repository
```bash
git clone <repo_url>
cd Worship_Session_Integration
