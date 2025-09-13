# Periodic Table Web App - Backend

A FastAPI backend for a high school IT class project featuring an interactive periodic table with flip cards, element information, and future chat/AI integration.

**Day 3.5 Update**: Now includes JWT-based authentication with role-based access control. Admin users can perform CRUD operations, while students can only read element data.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd TabelaPeriodica
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**:
   - API Base URL: http://localhost:8000
   - Interactive API Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Database Setup

The SQLite database is automatically created and initialized when you first run the server. No additional setup required!

- **Database file**: `periodic_table.db` (created in project directory)
- **Sample data**: Automatically includes Hydrogen and Helium
- **Admin user**: Automatically created (username: `admin`, password: `admin123`)
- **Management**: Use `python manage_db.py` to add more elements

### Authentication Setup

The system automatically creates an admin user on first run:
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin` (can perform all CRUD operations)

You can register additional users via the `/register` endpoint.

## 📚 API Endpoints

### Day 3.5 - Authentication + CRUD Operations

#### Public Endpoints (No Authentication Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/elements` | Get all elements from SQLite database |
| GET | `/elements/{symbol}` | Get specific element by symbol (case-insensitive) |
| POST | `/register` | Register a new user account |
| POST | `/login` | Login and get JWT token |
| GET | `/health` | Health check endpoint |

#### Admin-Only Endpoints (Requires JWT Token + Admin Role)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/elements` | Create a new element (Admin only) |
| PUT | `/elements/{symbol}` | Update an existing element (Admin only) |
| DELETE | `/elements/{symbol}` | Delete an element by symbol (Admin only) |

### Example API Responses

**Get all elements** (`GET /elements`):
```json
[
  {
    "id": 1,
    "symbol": "H",
    "name": "Hydrogen",
    "number": 1,
    "info": "The lightest and most abundant element in the universe. Essential for water and organic compounds."
  },
  {
    "id": 2,
    "symbol": "He",
    "name": "Helium",
    "number": 2,
    "info": "A noble gas that is lighter than air. Used in balloons and as a coolant for superconducting magnets."
  }
]
```

**Get specific element** (`GET /elements/H`):
```json
{
  "id": 1,
  "symbol": "H",
  "name": "Hydrogen",
  "number": 1,
  "info": "The lightest and most abundant element in the universe. Essential for water and organic compounds."
}
```

**Create element** (`POST /elements`):
```json
{
  "message": "Element 'O' created successfully",
  "element": {
    "id": 3,
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "Essential for respiration and combustion. Makes up about 21% of Earth's atmosphere."
  }
}
```

**Update element** (`PUT /elements/O`):
```json
{
  "message": "Element 'O' updated successfully",
  "element": {
    "id": 3,
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "Updated description: Essential for life and combustion processes."
  }
}
```

**Delete element** (`DELETE /elements/O`):
```json
{
  "message": "Element 'O' deleted successfully",
  "symbol": "O"
}
```

**Register user** (`POST /register`):
```json
{
  "message": "User 'student1' registered successfully",
  "user": {
    "id": 2,
    "username": "student1",
    "role": "student"
  }
}
```

**Login user** (`POST /login`):
```json
{
  "message": "Login successful for user 'admin'",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

## 🧪 Testing Authentication & CRUD Operations

### Authentication Testing

**1. Register a new user**:
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password123",
    "role": "student"
  }'
```

**2. Login as admin**:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**3. Save the JWT token from login response**:
```bash
# Copy the "access_token" value from the login response
# Example: TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Public Endpoints (No Authentication)

**4. Get all elements**:
```bash
curl -X GET http://localhost:8000/elements
```

**5. Get specific element**:
```bash
curl -X GET http://localhost:8000/elements/H
curl -X GET http://localhost:8000/elements/he  # Case-insensitive
```

### Admin-Only Endpoints (Requires JWT Token)

**6. Create new element (Admin only)**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "Essential for respiration and combustion. Makes up about 21% of Earth'\''s atmosphere."
  }'
```

**7. Update existing element (Admin only)**:
```bash
curl -X PUT http://localhost:8000/elements/O \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "info": "Updated description: Essential for life and combustion processes."
  }'
```

**8. Delete element (Admin only)**:
```bash
curl -X DELETE http://localhost:8000/elements/O \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Error Testing

**Try to create element without authentication**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "This will fail - no token"
  }'
```

**Try to create element with invalid token**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token" \
  -d '{
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "This will fail - invalid token"
  }'
```

**Try to login with wrong credentials**:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "wrongpassword"
  }'
```

**Try to register duplicate username**:
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123",
    "role": "student"
  }'
```

**Try to get non-existent element**:
```bash
curl -X GET http://localhost:8000/elements/X
```

## 🔗 Frontend Integration

### JavaScript Fetch Examples

**Authentication Helper**:
```javascript
// Store JWT token in localStorage
function setAuthToken(token) {
    localStorage.setItem('authToken', token);
}

function getAuthToken() {
    return localStorage.getItem('authToken');
}

function clearAuthToken() {
    localStorage.removeItem('authToken');
}

// Login function
async function login(username, password) {
    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            setAuthToken(data.access_token);
            console.log('Login successful:', data);
            return data;
        } else {
            const error = await response.json();
            console.error('Login failed:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Register function
async function register(username, password, role = 'student') {
    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, role })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Registration successful:', data);
            return data;
        } else {
            const error = await response.json();
            console.error('Registration failed:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}
```

**Public Endpoints (No Authentication Required)**:

**Get all elements**:
```javascript
async function fetchAllElements() {
    try {
        const response = await fetch('http://localhost:8000/elements');
        const elements = await response.json();
        console.log('All elements:', elements);
        return elements;
    } catch (error) {
        console.error('Error fetching elements:', error);
    }
}
```

**Get specific element**:
```javascript
async function fetchElement(symbol) {
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`);
        if (response.ok) {
            const element = await response.json();
            console.log('Element data:', element);
            return element;
        } else {
            console.error('Element not found');
        }
    } catch (error) {
        console.error('Error fetching element:', error);
    }
}
```

**Admin-Only Endpoints (Requires Authentication)**:

**Create new element (Admin only)**:
```javascript
async function createElement(elementData) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token. Please login first.');
    }
    
    try {
        const response = await fetch('http://localhost:8000/elements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(elementData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Element created:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Error creating element:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Error creating element:', error);
        throw error;
    }
}

// Usage example:
// First login as admin, then create element
async function exampleCreateElement() {
    try {
        await login('admin', 'admin123');
        await createElement({
            symbol: "N",
            name: "Nitrogen",
            number: 7,
            info: "Makes up 78% of Earth's atmosphere. Essential for proteins and DNA."
        });
    } catch (error) {
        console.error('Failed to create element:', error);
    }
}
```

**Update element (Admin only)**:
```javascript
async function updateElement(symbol, updateData) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token. Please login first.');
    }
    
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(updateData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Element updated:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Error updating element:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Error updating element:', error);
        throw error;
    }
}

// Usage example:
// First login as admin, then update element
async function exampleUpdateElement() {
    try {
        await login('admin', 'admin123');
        await updateElement("N", { info: "Updated description for Nitrogen" });
    } catch (error) {
        console.error('Failed to update element:', error);
    }
}
```

**Delete element (Admin only)**:
```javascript
async function deleteElement(symbol) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token. Please login first.');
    }
    
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Element deleted:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Error deleting element:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Error deleting element:', error);
        throw error;
    }
}

// Usage example:
// First login as admin, then delete element
async function exampleDeleteElement() {
    try {
        await login('admin', 'admin123');
        await deleteElement("N");
    } catch (error) {
        console.error('Failed to delete element:', error);
    }
}
```

## 📅 Development Roadmap

- **Day 1** ✅: Basic API with mock data
- **Day 2** ✅: SQLite database integration with real periodic table data
- **Day 3.0** ✅: Full CRUD operations for element management
- **Day 3.5** ✅: JWT authentication with role-based access control (CURRENT)
- **Day 4**: Chat/AI bot integration
- **Day 5**: Integration testing and polish
- **Day 6**: Presentation preparation

## 🧪 Testing

### Automated Testing with pytest

The project includes comprehensive automated tests using pytest. All tests are organized in the `tests/` directory.

#### Running Tests

**Run all tests**:
```bash
pytest -v
```

**Run specific test modules**:
```bash
# Test database operations
pytest tests/test_database.py -v

# Test API endpoints
pytest tests/test_elements.py -v

# Test authentication system
pytest tests/test_auth.py -v

# Test user roles and permissions
pytest tests/test_user_roles.py -v

# Test edge cases and error handling
pytest tests/test_edge_cases.py -v
```

**Run tests with coverage**:
```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage report
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

#### Test Structure

The test suite is organized into focused modules:

- **`tests/conftest.py`**: Shared test fixtures and configuration
- **`tests/test_database.py`**: SQLite database and SQLAlchemy model tests
- **`tests/test_elements.py`**: Elements API endpoint tests (GET, POST, PUT, DELETE)
- **`tests/test_auth.py`**: Authentication system tests (registration, login, JWT)
- **`tests/test_user_roles.py`**: Role-based access control tests (admin vs student)
- **`tests/test_edge_cases.py`**: Edge cases, boundary conditions, and error handling

#### Test Features

✅ **Database Tests**:
- Model creation and validation
- Unique constraints (symbol, username)
- Helper function testing
- Query operations

✅ **API Tests**:
- All CRUD operations
- Authentication requirements
- Error handling
- Case-insensitive searches

✅ **Authentication Tests**:
- Password hashing and verification
- JWT token creation and validation
- User registration and login
- Token-based access control

✅ **Role-Based Access Tests**:
- Admin permissions (full CRUD access)
- Student permissions (read-only access)
- Unauthenticated access restrictions

✅ **Edge Case Tests**:
- Boundary value testing
- Invalid input handling
- Concurrent operations
- Error recovery

#### Test Configuration

Tests use an in-memory SQLite database for isolation and speed. Each test runs in a clean environment with:
- Fresh database tables
- Sample data fixtures
- Admin and student user accounts
- JWT tokens for authentication testing

### Manual Testing

#### Quick API Test

**Test basic functionality**:
```bash
# Get all elements
curl http://localhost:8000/elements

# Get specific element
curl http://localhost:8000/elements/H

# Register new user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123", "role": "student"}'

# Login as admin
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Interactive Testing

**Use the interactive API documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Development Commands

```bash
# Run development server with auto-reload
uvicorn main:app --reload

# Run on specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run all tests
pytest -v

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_elements.py -v

# Test basic API functionality (legacy)
python tests/test_api.py

# Test comprehensive CRUD operations (legacy)
python tests/test_crud.py

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

## 📁 Project Structure

```
TabelaPeriodica/
├── main.py              # FastAPI application with authentication & CRUD
├── models.py            # SQLAlchemy database models (Element, User)
├── schemas.py           # Pydantic schemas for validation
├── auth.py              # Authentication & JWT functions
├── manage_db.py         # Database management script
├── requirements.txt     # Python dependencies
├── periodic_table.db    # SQLite database (created automatically)
├── tests/               # Comprehensive test suite
│   ├── conftest.py      # Shared test fixtures and configuration
│   ├── test_database.py # Database and SQLAlchemy model tests
│   ├── test_elements.py # Elements API endpoint tests
│   ├── test_auth.py     # Authentication system tests
│   ├── test_user_roles.py # Role-based access control tests
│   ├── test_edge_cases.py # Edge cases and error handling tests
│   ├── test_api.py      # Legacy basic API testing script
│   └── test_crud.py     # Legacy CRUD testing script
└── README.md           # This file
```

## 🗄️ Database Management

### Adding Elements

Use the database management script to add more elements:

```bash
python manage_db.py
```

This interactive script allows you to:
- Add sample elements (Lithium, Carbon, Nitrogen, Oxygen, Fluorine)
- Add custom elements with your own data
- List all elements in the database
- Reset the database if needed

### Adding Elements Programmatically

You can also add elements directly in Python:

```python
from models import add_element

# Add a new element
add_element(
    symbol="Na",
    name="Sodium", 
    number=11,
    info="Essential for nerve function and muscle contraction."
)
```

### Database Schema

The `Element` table has the following structure:
- `id`: Primary key (auto-increment)
- `symbol`: Chemical symbol (unique, e.g., "H", "He")
- `name`: Full element name (e.g., "Hydrogen", "Helium")
- `number`: Atomic number (e.g., 1, 2)
- `info`: Description/information about the element

## 🤝 Team Collaboration

This backend is designed to work with the frontend team's HTML/CSS/JS implementation. The API provides clean JSON responses that can be easily consumed by JavaScript fetch calls.

**For Frontend Developers**: Use the JavaScript examples above to integrate with this API. The CORS middleware is configured to allow requests from any origin during development.

## 🐛 Troubleshooting

**Port already in use**:
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001 --reload
```

**Module not found errors**:
```bash
# Make sure you're in the project directory
cd TabelaPeriodica

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Notes

- This is Day 3.5 implementation with JWT authentication and role-based access control
- CORS is configured for development (allows all origins)
- Database is automatically created and initialized on first run
- Case-insensitive element symbol search (e.g., "h", "H", "he", "He" all work)
- Pydantic validation ensures data integrity
- Duplicate symbol/atomic number prevention
- JWT tokens expire after 30 minutes
- Admin users can perform CRUD operations, students can only read
- Default admin account: username="admin", password="admin123"
- Use `python manage_db.py` to easily add more elements
- SQLAlchemy 2.0.43 for Python 3.13 compatibility
