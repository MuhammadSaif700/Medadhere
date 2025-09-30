# MedAdhere Frontend

A modern, responsive web interface for the MedAdhere AI-powered medication adherence system.

## Features

### 🎯 Dashboard
- Real-time adherence statistics
- Progress tracking
- Upcoming medication reminders
- Activity timeline

### 📸 Pill Identification
- Upload pill images for AI identification
- Real-time confidence scoring
- Medication verification
- Dose logging integration

### 📅 Medication Schedule
- Complete medication management
- Schedule visualization
- Dosage instructions
- Medication editing

### 📊 Reports & Analytics
- Adherence rate tracking
- Missed dose analysis
- Streak monitoring
- Personalized recommendations

### 🔍 Pill Database Search
- Comprehensive pill database
- Search by name, color, shape, imprint
- Detailed medication information

## Technology Stack

- **Frontend Framework**: React 18 (via CDN)
- **Styling**: Tailwind CSS 2.2.19
- **Icons**: Font Awesome 6.0
- **Build Tool**: Babel Standalone (for JSX transformation)
- **API Integration**: Fetch API with FastAPI backend

## Quick Start

1. **Prerequisites**
   - MedAdhere backend server running on `http://localhost:8000`
   - Modern web browser with JavaScript enabled

2. **Launch Frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend
   
   # Open in browser (choose one method)
   
   # Method 1: Direct file opening
   start index.html
   
   # Method 2: Simple HTTP server
   python -m http.server 3000
   # Then visit: http://localhost:3000
   
   # Method 3: VS Code Live Server extension
   # Right-click index.html → "Open with Live Server"
   ```

3. **Access Application**
   - Direct file: `file:///path/to/frontend/index.html`
   - HTTP server: `http://localhost:3000`
   - Live Server: Usually `http://127.0.0.1:5500/frontend/`

## Architecture

### Component Structure
```
App (Main Component)
├── Navigation (Top navigation bar)
├── Dashboard (Overview & statistics)
├── PillIdentification (Camera & AI identification)
├── MedicationSchedule (Schedule management)
├── Reports (Analytics & tracking)
└── PillSearch (Database search)
```

### API Integration
- **Base URL**: `http://localhost:8000`
- **Endpoints Used**:
  - `/api/v1/pills/identify` - Pill identification
  - `/api/v1/pills/database` - Pill database search
  - `/api/v1/medications/schedule/{patient_id}` - Medication schedule
  - `/api/v1/adherence/stats/{patient_id}` - Adherence statistics
  - `/api/v1/adherence/report/{patient_id}` - Detailed reports

### State Management
- React Hooks (`useState`, `useEffect`)
- Component-level state management
- API data caching in component state

## Features Detail

### Responsive Design
- Mobile-first approach
- Tailwind CSS responsive utilities
- Adaptive layouts for all screen sizes
- Touch-friendly interfaces

### Real-time Updates
- Live adherence statistics
- Automatic data refresh
- Progress indicators
- Loading states

### User Experience
- Intuitive navigation
- Clear visual feedback
- Accessibility considerations
- Error handling with fallbacks

### Mock Data Fallbacks
- Graceful degradation when API unavailable
- Demo data for offline testing
- Development-friendly setup

## Browser Support

- **Modern Browsers**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **JavaScript**: ES6+ features used
- **CSS**: Modern Flexbox and Grid support required

## Development Notes

### CDN Dependencies
All dependencies loaded via CDN for simplicity:
- React 18 (development build for debugging)
- Tailwind CSS (complete framework)
- Font Awesome (full icon set)
- Babel Standalone (JSX transformation)

### API Error Handling
- Automatic fallback to mock data
- Network error recovery
- User-friendly error messages
- Development logging

### Performance Considerations
- Component-based architecture
- Efficient re-rendering with React hooks
- Image optimization for pill photos
- Minimal external dependencies

## Customization

### Styling
- Modify Tailwind classes in components
- Add custom CSS in `<style>` tags if needed
- Color scheme defined in Tailwind utilities

### API Configuration
- Change `API_BASE_URL` constant for different backend
- Modify endpoint paths in fetch calls
- Add authentication headers if required

### Features
- Add new components for additional features
- Extend existing components with new functionality
- Integrate with additional APIs as needed

## Security Considerations

- No sensitive data stored in frontend
- API calls use relative URLs when possible
- File uploads handled securely
- No inline scripts (using React components)

## Deployment Options

### Static Hosting
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront

### Development Server
- Python `http.server`
- Node.js `serve` package
- VS Code Live Server extension

### Production Considerations
- Enable HTTPS for file uploads
- Configure CORS properly on backend
- Optimize assets for production
- Add service worker for offline functionality

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend has CORS configured
   - Check network tab for request details
   - Verify API URL is correct

2. **Image Upload Issues**
   - Check file size limits
   - Verify image format support
   - Ensure backend endpoint accepts files

3. **Mock Data Showing**
   - Backend server not running
   - Network connectivity issues
   - API endpoints returning errors

### Debug Tips
- Open browser developer tools
- Check console for JavaScript errors
- Monitor network tab for API calls
- Verify backend server is running on port 8000

## Future Enhancements

- Real-time notifications
- Offline functionality with service workers
- Progressive Web App (PWA) features
- Advanced analytics and charts
- Multi-language support
- Dark mode theme
- Voice commands integration