# Periodic Table Web App - Backend

A FastAPI backend for a high school IT class project featuring an interactive periodic table with flip cards, element information, and future chat/AI integration.

**Day 3.9 Update**: Now includes full CRUD operations for element management with Pydantic validation and comprehensive error handling.

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
- **Management**: Use `python manage_db.py` to add more elements

## 📚 API Endpoints

### Day 3.9 - Full CRUD Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/elements` | Get all elements from SQLite database |
| GET | `/elements/{symbol}` | Get specific element by symbol (case-insensitive) |
| POST | `/elements` | Create a new element |
| PUT | `/elements/{symbol}` | Update an existing element |
| DELETE | `/elements/{symbol}` | Delete an element by symbol |
| GET | `/health` | Health check endpoint |

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

## 🧪 Testing CRUD Operations

### Using curl Commands

**1. Get all elements**:
```bash
curl -X GET http://localhost:8000/elements
```

**2. Get specific element**:
```bash
curl -X GET http://localhost:8000/elements/H
curl -X GET http://localhost:8000/elements/he  # Case-insensitive
```

**3. Create new element**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "O",
    "name": "Oxygen",
    "number": 8,
    "info": "Essential for respiration and combustion. Makes up about 21% of Earth'\''s atmosphere."
  }'
```

**4. Update existing element**:
```bash
curl -X PUT http://localhost:8000/elements/O \
  -H "Content-Type: application/json" \
  -d '{
    "info": "Updated description: Essential for life and combustion processes."
  }'
```

**5. Delete element**:
```bash
curl -X DELETE http://localhost:8000/elements/O
```

### Error Testing

**Try to create duplicate element**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "H",
    "name": "Hydrogen",
    "number": 1,
    "info": "This will fail - already exists"
  }'
```

**Try to get non-existent element**:
```bash
curl -X GET http://localhost:8000/elements/X
```

## 🔗 Frontend Integration

### JavaScript Fetch Examples

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

**Create new element**:
```javascript
async function createElement(elementData) {
    try {
        const response = await fetch('http://localhost:8000/elements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
        }
    } catch (error) {
        console.error('Error creating element:', error);
    }
}

// Usage example:
createElement({
    symbol: "N",
    name: "Nitrogen",
    number: 7,
    info: "Makes up 78% of Earth's atmosphere. Essential for proteins and DNA."
});
```

**Update element**:
```javascript
async function updateElement(symbol, updateData) {
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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
        }
    } catch (error) {
        console.error('Error updating element:', error);
    }
}

// Usage example:
updateElement("N", { info: "Updated description for Nitrogen" });
```

**Delete element**:
```javascript
async function deleteElement(symbol) {
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Element deleted:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Error deleting element:', error);
        }
    } catch (error) {
        console.error('Error deleting element:', error);
    }
}

// Usage example:
deleteElement("N");
```

## 📅 Development Roadmap

- **Day 1** ✅: Basic API with mock data
- **Day 2** ✅: SQLite database integration with real periodic table data
- **Day 3.9** ✅: Full CRUD operations for element management (CURRENT)
- **Day 4**: User login and authentication system (restrict CRUD to admin users)
- **Day 5**: Chat/AI bot integration
- **Day 6**: Integration testing and polish
- **Day 7**: Presentation preparation

## 🛠️ Development Commands

```bash
# Run development server with auto-reload
uvicorn main:app --reload

# Run on specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Test basic API functionality
python test_api.py

# Test comprehensive CRUD operations
python test_crud.py

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

## 📁 Project Structure

```
TabelaPeriodica/
├── main.py              # FastAPI application with CRUD endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for request/response validation
├── manage_db.py         # Database management script
├── test_api.py          # Basic API testing script
├── test_crud.py         # Comprehensive CRUD testing script
├── requirements.txt     # Python dependencies
├── periodic_table.db    # SQLite database (created automatically)
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

- This is Day 3.9 implementation with full CRUD operations
- CORS is configured for development (allows all origins)
- Database is automatically created and initialized on first run
- Case-insensitive element symbol search (e.g., "h", "H", "he", "He" all work)
- Pydantic validation ensures data integrity
- Duplicate symbol/atomic number prevention
- Authentication will be added in Day 4
- Use `python manage_db.py` to easily add more elements
- SQLAlchemy 2.0.43 for Python 3.13 compatibility
