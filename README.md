# Kings Queens Voting Website

A beautiful Flask-based voting website for the GUSTO Thadingyut Festival King and Queen competition.

## Features

- 🎨 **Beautiful UI**: Modern, responsive design with Tailwind CSS
- 👑 **King & Queen Voting**: Vote for your favorite candidates
- 📊 **Real-time Results**: View live voting results
- 🖼️ **Candidate Profiles**: Detailed candidate information with image galleries
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🗄️ **MySQL Database**: Persistent vote storage with Aiven cloud database

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

The application will automatically create the database tables and populate them with candidate data when you first run it.

**Database Configuration:**
- Host: `mysql-3f32765c-votingwebsite.i.aivencloud.com`
- Port: `19840`
- Database: `votingdb`
- SSL Certificate: `ca.pem` (if provided by Aiven)

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 4. Test the System

```bash
python test_voting.py
```

## How to Use

### For Voters

1. **Visit the Home Page**: Navigate to `http://localhost:5000`
2. **View Candidates**: Click "Candidate" to see all King and Queen candidates
3. **Vote**: Click the "Vote" button on any candidate card
4. **View Results**: Click "Voting Result" to see current standings
5. **Candidate Details**: Click "View more" to see detailed candidate profiles

### For Administrators

- **Monitor Votes**: Check the `/results` page for real-time vote counts
- **Database Access**: Connect directly to the MySQL database to view detailed voting data

## File Structure

```
Voting Website/
├── app.py                 # Main Flask application
├── requirements.txt      # Python dependencies
├── test_voting.py        # Test script
├── templates/            # HTML templates
│   ├── home.html         # Home page
│   ├── candidate-king.html # Candidates page
│   ├── viewmore.html     # Candidate details
│   ├── voting_result.html # Results page
│   ├── about_us.html     # About page
│   ├── lantern.html      # Lantern page
│   ├── final.html        # Final page
│   └── winner.html       # Winner page
├── templates/img/        # Images and assets
│   ├── Kings/           # King candidate images
│   ├── Queen/           # Queen candidate images
│   ├── King_Viewmore/   # King detail images
│   └── Queen_Viewmore/  # Queen detail images
└── venv/                # Virtual environment
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/candidates` | GET | Candidates page with voting |
| `/viewmore` | GET | Candidate details page |
| `/vote` | POST | Submit a vote |
| `/results` | GET | Voting results |
| `/lantern` | GET | Lantern page |
| `/about` | GET | About page |
| `/final` | GET | Final page |
| `/winner` | GET | Winner page |

## Voting System

### How Votes Work

1. **Vote Submission**: Users click the "Vote" button on a candidate card
2. **AJAX Request**: JavaScript sends the vote to `/vote` endpoint
3. **Database Update**: Vote count is incremented in the MySQL database
4. **User Feedback**: Success/error message is displayed
5. **Redirect**: User is redirected to results page after successful vote

### Database Schema

**Kings Table:**
```sql
CREATE TABLE kings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    batch VARCHAR(50),
    bio TEXT,
    image_path VARCHAR(200),
    vote_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Queens Table:**
```sql
CREATE TABLE queens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    batch VARCHAR(50),
    bio TEXT,
    image_path VARCHAR(200),
    vote_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Customization

### Adding New Candidates

1. **Database**: Add new records to `kings` or `queens` tables
2. **Images**: Add candidate images to appropriate folders
3. **Restart**: Restart the Flask application

### Styling Changes

- **CSS**: Modify Tailwind classes in HTML templates
- **Colors**: Update color schemes in the CSS sections
- **Layout**: Adjust grid layouts and responsive breakpoints

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check Aiven credentials
   - Verify SSL certificate file exists
   - Ensure network connectivity

2. **Images Not Loading**
   - Check file paths in templates
   - Verify image files exist in correct directories
   - Check file permissions

3. **Voting Not Working**
   - Check browser console for JavaScript errors
   - Verify Flask app is running
   - Check database connection

### Debug Mode

Enable debug mode in `app.py`:
```python
app.run(debug=True)
```

## Security Considerations

- **Input Validation**: All vote submissions are validated
- **SQL Injection**: Using parameterized queries
- **Rate Limiting**: Consider implementing vote rate limiting
- **Authentication**: Add user authentication if needed

## Deployment

### Production Deployment

1. **Environment Variables**: Use environment variables for database credentials
2. **SSL Certificate**: Ensure proper SSL configuration
3. **Static Files**: Configure web server for static file serving
4. **Database Backup**: Implement regular database backups

### Heroku Deployment

1. Create `Procfile`:
   ```
   web: python app.py
   ```

2. Add to `requirements.txt`:
   ```
   gunicorn==20.1.0
   ```

3. Deploy:
   ```bash
   git add .
   git commit -m "Deploy voting website"
   git push heroku main
   ```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Run the test script to verify functionality
3. Check Flask application logs
4. Verify database connectivity

## License

This project is created for the GUSTO Thadingyut Festival voting system.

---

**Happy Voting! 🗳️👑👸**
