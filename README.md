# 🌱 EcoLink - Sustainable File Management Platform

EcoLink is a comprehensive web application that helps organizations and individuals manage their digital files sustainably. It provides intelligent duplicate detection, environmental impact analysis, and actionable recommendations to reduce energy consumption and CO2 emissions from digital storage.

## 🌟 Key Features

- **🔍 Smart Duplicate Detection**: SHA-256 based duplicate detection prevents redundant storage
- **📊 Environmental Impact Analysis**: Real-time calculation of kWh consumption and CO2 emissions
- **💡 AI-Driven Recommendations**: Smart suggestions for compression, archiving, and file optimization
- **📈 Analytics Dashboard**: Comprehensive insights into storage patterns and environmental impact
- **🔒 Secure File Storage**: S3-compatible storage with presigned URLs for secure uploads
- **⚡ Real-time Processing**: Asynchronous file processing with Celery workers

## 🏗️ Technology Stack

### Backend
- **Django 5** with Django REST Framework
- **MySQL/PostgreSQL** for data persistence
- **Celery + Redis** for async task processing
- **S3-compatible storage** (MinIO for development)

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Material-UI** for modern UI components

### Infrastructure
- **Docker Compose** for containerized deployment
- **Nginx** as reverse proxy
- **JWT Authentication** with refresh tokens

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/punam06/EcoLink.git
   cd EcoLink
   ```

2. **Navigate to the project directory**
   ```bash
   cd project
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py shell < seed_data.py
   ```

5. **Set up MinIO storage**
   - Open MinIO Console: http://localhost:9001
   - Login with credentials: `minioadmin` / `minioadmin`
   - Create a bucket named "ecolink"

6. **Access the application**
   - **Frontend**: http://localhost
   - **Backend API**: http://localhost/api
   - **MinIO Console**: http://localhost:9001

### Demo Credentials
- **Username**: demo
- **Password**: demo123

## 📁 Project Structure

```
EcoLink/
├── project/                    # Main application directory
│   ├── backend/               # Django backend application
│   │   ├── ecolink/          # Core Django project settings
│   │   ├── files/            # File management application
│   │   ├── analytics/        # Environmental analytics
│   │   ├── authentication/   # User authentication
│   │   └── requirements.txt  # Python dependencies
│   ├── frontend/             # React frontend application
│   │   ├── src/
│   │   │   ├── api/         # API client utilities
│   │   │   ├── components/  # Reusable React components
│   │   │   ├── contexts/    # React context providers
│   │   │   ├── pages/       # Main page components
│   │   │   └── types/       # TypeScript type definitions
│   │   └── package.json     # Node.js dependencies
│   ├── nginx/               # Nginx reverse proxy configuration
│   ├── mysql/               # MySQL database initialization
│   └── docker-compose.yml   # Docker services orchestration
└── README.md                # This file
```

## 🌍 Environmental Impact

EcoLink calculates the environmental impact of your digital storage:

### Energy Consumption
```
kWh = (file_size_gb) × REGION_KWH_PER_GB
```

### CO2 Emissions
```
CO2_grams = kWh × REGION_CO2_G_PER_KWH
```

The platform provides actionable insights to help reduce your digital carbon footprint through:
- Duplicate file elimination
- File compression recommendations
- Storage optimization strategies
- Usage pattern analysis

## 🔄 File Upload Workflow

1. **Request Upload**: Client requests a presigned upload URL
2. **Hash Calculation**: SHA-256 hash computed client-side
3. **S3 Upload**: Direct upload to S3 using presigned URL
4. **Commit Process**: Server processes and analyzes the file
5. **Impact Analysis**: Environmental impact calculated and stored
6. **Recommendations**: AI-driven optimization suggestions generated

## 🛠️ Development

For detailed development setup instructions, please see the [Project README](./project/README.md).

### Key Development Commands

```bash
# Start development environment
cd project && docker-compose up -d

# Run backend tests
cd project/backend && python manage.py test

# Run frontend tests
cd project/frontend && npm run test

# Format backend code
cd project/backend && black . && ruff check .

# Format frontend code
cd project/frontend && npm run lint
```

## 📚 API Documentation

The application provides a RESTful API with the following key endpoints:

- **Authentication**: `/api/auth/login/`, `/api/auth/refresh/`
- **File Management**: `/api/v1/files/` (CRUD operations)
- **Analytics**: `/api/v1/analytics/summary/`, `/api/v1/analytics/impact-trend/`
- **Recommendations**: `/api/v1/recommendations/`

For detailed API documentation, please refer to the [Project README](./project/README.md).

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards
- **Backend**: Black formatting, Ruff linting, comprehensive tests
- **Frontend**: ESLint, Prettier, TypeScript strict mode
- **Commits**: Conventional commit messages
- **Documentation**: Update README and inline documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern web technologies and best practices
- Environmental calculations based on industry research and standards
- UI components from Material-UI ecosystem
- Charts and visualizations powered by Recharts

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/punam06/EcoLink/issues)
- 📖 **Documentation**: Check the `/project/README.md` for detailed documentation
- 💬 **Discussions**: [GitHub Discussions](https://github.com/punam06/EcoLink/discussions)

---

**EcoLink** - Making digital storage more sustainable, one file at a time. 🌱

*Reduce your digital carbon footprint while maintaining efficient file management.*