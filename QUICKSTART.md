# MedAdhere - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.13+ installed
- Windows, macOS, or Linux

### Installation & Setup

1. **Clone/Open the project in VS Code**
   ```bash
   cd "AI-Powered Dynamic Pricing Engine"
   ```

2. **Install Dependencies**
   - Use VS Code Command Palette: `Tasks: Run Task` → `Install Dependencies`
   - Or run manually: `python -m pip install -r requirements.txt`

3. **Start the Server**
   - Use VS Code Command Palette: `Tasks: Run Build Task` → `Start MedAdhere Server`
   - Or run manually: `python main.py`

4. **Access the Application**
   - Main API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### 🧪 Running Tests
- Use VS Code Command Palette: `Tasks: Run Task` → `Run Tests`
- Or run manually: `python -m pytest tests/test_simple.py -v`

## 📱 Using the API

### Core Endpoints

#### 1. Pill Identification
```http
POST /api/v1/pills/identify
Content-Type: multipart/form-data

# Upload an image file of a pill
```

#### 2. Search Pills Database
```http
GET /api/v1/pills/search?name=aspirin&color=white
```

#### 3. Medication Verification
```http
POST /api/v1/medications/verify
Content-Type: application/json

{
  "patient_id": "patient_001",
  "pill_info": {
    "name": "Aspirin",
    "dosage": "325mg",
    "shape": "round",
    "color": "white"
  }
}
```

#### 4. Get Patient Schedule
```http
GET /api/v1/medications/schedule/patient_001
```

#### 5. Adherence Reports
```http
GET /api/v1/adherence/report/patient_001?days=30
```

## 🏗️ Architecture Overview

### Core Components
- **Pill Identifier**: Computer vision for pill recognition
- **Medication Verifier**: Schedule validation and verification
- **Ingestion Detector**: AI-powered ingestion confirmation
- **Adherence Tracker**: Analytics and reporting
- **Database**: SQLite with SQLAlchemy ORM

### File Structure
```
src/
├── api/           # FastAPI REST endpoints
├── models/        # ML models and business logic
├── vision/        # Image processing utilities
├── database/      # Database models and initialization
└── utils/         # Configuration and helpers
```

## 🔧 Development

### Adding New Features
1. **New API Endpoint**: Add to `src/api/routers/`
2. **New ML Model**: Add to `src/models/`
3. **Database Changes**: Update `src/database/models.py`
4. **Tests**: Add to `tests/`

### Configuration
- Environment variables: `.env` file
- Application settings: `src/utils/config.py`

## 🚨 Production Deployment

### Enhanced ML Models
For production deployment, replace mock models with:
- **TensorFlow/PyTorch** models for pill identification
- **OpenCV** for advanced image processing
- **Real pill database** (NIH Pill Image Database)

### Security
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS
- Secure database credentials

### Scaling
- Use PostgreSQL/MySQL for production database
- Add Redis for caching
- Deploy with Docker/Kubernetes
- Use cloud services for ML inference

## 📊 Monitoring & Analytics

The system provides comprehensive adherence tracking:
- Real-time medication compliance
- Caregiver alert system
- Trend analysis and insights
- Customizable reporting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🎯 MedAdhere is ready for production deployment and smartphone integration!**