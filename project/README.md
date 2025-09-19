# 🌱 EcoLink - Sustainable File Management Platform

EcoLink is a web application that helps organizations and individuals manage their digital files sustainably by detecting duplicates, measuring environmental impact, and providing recommendations to reduce energy consumption and CO2 emissions.

## 🎯 Features

### Core Functionality
- **File Upload & Storage**: Secure file upload to S3/MinIO with presigned URLs
- **Duplicate Detection**: SHA-256 based duplicate detection to prevent redundant storage
- **Environmental Impact Analysis**: Calculate kWh consumption and CO2 emissions per file
- **Smart Recommendations**: AI-driven suggestions for compression, archiving, and sharing
- **Real-time Analytics**: Dashboard with CO2 savings, storage metrics, and impact trends

### Technical Features
- **Backend**: Django 5 + Django REST Framework + PostgreSQL/MySQL
- **Frontend**: React 18 + TypeScript + Vite + Material-UI
- **Authentication**: JWT-based authentication with refresh tokens
- **File Processing**: Async processing with Celery + Redis
- **Storage**: S3-compatible storage (MinIO for development)
- **API**: RESTful API with proper throttling and validation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │  Django API     │    │   Celery        │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Workers)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌─────────┐              ┌─────────┐              ┌─────────┐
    │ Nginx   │              │ MySQL   │              │ Redis   │
    │ Proxy   │              │Database │              │ Broker  │
    └─────────┘              └─────────┘              └─────────┘
                                      │
                                ┌─────────────┐
                                │    MinIO    │
                                │  (S3 Compat)│
                                └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecolink
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize the database**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py shell < seed_data.py
   ```

4. **Create MinIO bucket**
   - Open MinIO Console: http://localhost:9001
   - Login: minioadmin / minioadmin
   - Create bucket named "ecolink"

5. **Access the application**
   - Frontend: http://localhost (via Nginx)
   - Backend API: http://localhost/api
   - MinIO Console: http://localhost:9001

### Demo Credentials
- **Username**: demo
- **Password**: demo123

## 🛠️ Development Setup

### Backend Development

1. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp ../.env.sample .env
   # Edit .env with your local settings
   ```

3. **Start supporting services**
   ```bash
   docker-compose up mysql redis minio -d
   ```

4. **Run migrations and seed data**
   ```bash
   python manage.py migrate
   python manage.py shell < seed_data.py
   ```

5. **Start Django development server**
   ```bash
   python manage.py runserver
   ```

6. **Start Celery worker (in another terminal)**
   ```bash
   celery -A ecolink worker --loglevel=info
   ```

### Frontend Development

1. **Set up Node.js environment**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

### File Management
- `GET /api/v1/files/` - List user's files
- `GET /api/v1/files/{id}/` - Get file details
- `POST /api/v1/files/request-upload-url/` - Get presigned upload URL
- `POST /api/v1/files/commit/` - Commit file upload and trigger analysis
- `GET /api/v1/files/{id}/download-url/` - Get presigned download URL

### Analytics
- `GET /api/v1/analytics/summary/` - Get environmental impact summary
- `GET /api/v1/analytics/file-types/` - Get file type breakdown
- `GET /api/v1/analytics/impact-trend/` - Get impact trend data

### Recommendations
- `GET /api/v1/recommendations/` - Get user's recommendations

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
MYSQL_HOST=localhost
MYSQL_DB=ecolink
MYSQL_USER=ecolink_user
MYSQL_PASSWORD=your-password
S3_ENDPOINT=http://localhost:9000
S3_BUCKET=ecolink
REGION_KWH_PER_GB=0.006
REGION_CO2_G_PER_KWH=400
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📁 Project Structure

```
ecolink/
├── backend/                 # Django backend
│   ├── ecolink/            # Main Django project
│   ├── files/              # File management app
│   ├── analytics/          # Analytics app
│   ├── authentication/     # Auth app
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend Docker config
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── pages/         # Page components
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend Docker config
├── nginx/                  # Nginx configuration
├── mysql/                  # MySQL initialization
├── docker-compose.yml      # Docker services
├── .env.sample            # Environment template
└── README.md              # This file
```

## 🔄 File Upload Flow

1. **Client requests upload URL**
   ```
   POST /api/v1/files/request-upload-url/
   { "filename": "document.pdf", "content_type": "application/pdf" }
   ```

2. **Client calculates SHA-256** (browser-side with Web Crypto API)

3. **Client uploads to S3** using presigned URL (PUT request)

4. **Client commits upload**
   ```
   POST /api/v1/files/commit/
   { "bucket": "ecolink", "key": "uploads/1/abc123_document.pdf", 
     "filename": "document.pdf", "size_bytes": 1048576 }
   ```

5. **Server triggers analysis** (Celery task)
   - Downloads file from S3
   - Computes SHA-256 hash
   - Detects MIME type
   - Checks for duplicates
   - Calculates environmental impact
   - Generates recommendations

## 🌍 Environmental Impact Calculation

### Energy Consumption
```
kWh = (file_size_gb) × REGION_KWH_PER_GB
```

### CO2 Emissions
```
CO2_grams = kWh × REGION_CO2_G_PER_KWH
```

### Impact Score (0-100)
Based on file size, CO2 emissions, and duplicate status.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

### Code Standards
- **Backend**: Black formatting, Ruff linting
- **Frontend**: ESLint, Prettier, TypeScript strict mode
- **Commits**: Conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Django, React, and modern web technologies
- Environmental impact calculations based on industry research
- Icons from Material-UI Icons
- Charts powered by Recharts

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the documentation in the `/docs` folder
- Contact the development team

---

**EcoLink** - Making digital storage more sustainable, one file at a time. 🌱