# Social Network Platform

A full-stack social networking platform built with **Vue.js** on the frontend and **FastAPI** on the backend.  
It supports user authentication, posts with image uploads, and scalable data storage using **PostgreSQL** (production) and **SQLite** (development), with **Cloudinary** handling media storage.

---

## Tech Stack

### Frontend
- **Vue.js**
- Vue Router
- Primevue
- TailwindCSS

### Backend
- **FastAPI**
- SQLAlchemy
- Pydantic
- Uvicorn

### Database
- **PostgreSQL** (production)
- **SQLite** (local development)

### Media Storage
- **Cloudinary** (image hosting)

---

## Features

- User authentication (JWT-based)
- Create, edit, and delete posts
- Image uploads via Cloudinary
- User profiles
- RESTful API


## Startup of local deployment

### Prerequisites

The only software prerequisite needed is Docker.

However, you will need cloudinary API credentials. You can get them at [the following url](https://cloudinary.com)

### Environment

To start the project, you will need to have one or two `.env` files, depending on which version you want to start

This is the full list of environment variables used in the project:

```dotenv
SECRET_KEY="your JWT secret key here" # REQUIRED
CLOUDINARY_CLOUD_NAME="cloudinary.com" # REQUIRED
CLOUDINARY_API_KEY="cloudinary.com" # REQUIRED
CLOUDINARY_API_SECRET="cloudinary.com" # REQUIRED
CLOUDINARY_PFP_FOLDER="fastapi_uploads_pfp" # NOT required
FRONTEND_URL="http://localhost:5173" # NOT required
JWT_EXPIRATION_HOURS="24" # NOT required
DATABASE_URL="some postgres db conn string here" # If not provided defaults to creating a .sqlite file
FLASK_ENV="development" # Either development or production
```

But for the production version, you will need another `.env` file located in the `client/` directory, with only one variable, `VITE_API_URL`, corresponding to your server routing config

As for the Nginx config, it's only needed for production purposes, so here's an example one:

`client/nginx.conf`:
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri /index.html;
    }
}
```

Change this config to your own preferences/needs

### Startup

Command to run the development version:

`docker compose -f docker-compose.dev.yaml up --build`

Command to run the production version:

`docker compose -f docker-compose.prod.yaml up --build`
