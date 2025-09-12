"""
Database Models for Periodic Table Web App
SQLAlchemy ORM models for element data storage

This file defines the database structure using SQLAlchemy ORM
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class for our models
Base = declarative_base()

class Element(Base):
    """
    Element model representing a chemical element in the periodic table
    
    This model stores the basic information about each chemical element
    that will be displayed on the frontend flip cards
    """
    __tablename__ = "elements"
    
    # Primary key - unique identifier for each element
    id = Column(Integer, primary_key=True, index=True)
    
    # Chemical symbol (e.g., "H", "He", "C") - must be unique
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    
    # Full element name (e.g., "Hydrogen", "Helium", "Carbon")
    name = Column(String(50), nullable=False)
    
    # Atomic number (e.g., 1, 2, 6)
    number = Column(Integer, nullable=False)
    
    # Description/information about the element
    info = Column(String(500), nullable=True)
    
    def __repr__(self):
        """String representation of the element for debugging"""
        return f"<Element(symbol='{self.symbol}', name='{self.name}', number={self.number})>"
    
    def to_dict(self):
        """Convert element to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "number": self.number,
            "info": self.info
        }

class User(Base):
    """
    User model for authentication and authorization
    
    This model stores user account information including
    username, hashed password, and role for access control
    """
    __tablename__ = "users"
    
    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)
    
    # Username - must be unique
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # Password hash - stores bcrypt hashed password
    password_hash = Column(String(255), nullable=False)
    
    # User role - determines access permissions
    # "admin" can perform CRUD operations, "student" can only read
    role = Column(String(20), nullable=False, default="student")
    
    def __repr__(self):
        """String representation of the user for debugging"""
        return f"<User(username='{self.username}', role='{self.role}')>"
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization (without password)"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

# Database configuration
DATABASE_URL = "sqlite:///./periodic_table.db"

# Create database engine
# SQLite database will be created in the project directory
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function to get database session
    
    This function creates a new database session for each request
    and ensures it's properly closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables
    
    This function creates the elements table in the SQLite database
    Call this once when setting up the database
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def add_element(symbol: str, name: str, number: int, info: str = None):
    """
    Helper function to add a new element to the database
    
    Args:
        symbol (str): Chemical symbol (e.g., "H", "He")
        name (str): Full element name (e.g., "Hydrogen", "Helium")
        number (int): Atomic number (e.g., 1, 2)
        info (str, optional): Description of the element
    
    Returns:
        Element: The created element object
    """
    db = SessionLocal()
    try:
        # Create new element
        new_element = Element(
            symbol=symbol,
            name=name,
            number=number,
            info=info
        )
        
        # Add to database
        db.add(new_element)
        db.commit()  # Save changes to database
        db.refresh(new_element)  # Get the element with its ID
        
        print(f"✅ Added element: {new_element.symbol} - {new_element.name}")
        return new_element
        
    except Exception as e:
        db.rollback()  # Undo changes if error occurs
        print(f"❌ Error adding element {symbol}: {e}")
        raise e
    finally:
        db.close()

def init_sample_data():
    """
    Initialize database with sample element data
    
    This function adds a few example elements to get started
    More elements can be added later using the add_element function
    """
    db = SessionLocal()
    try:
        # Check if elements already exist
        if db.query(Element).count() > 0:
            print("📋 Database already contains elements, skipping initialization")
            return
        
        # Add sample elements
        sample_elements = [
            {
                "symbol": "H",
                "name": "Hydrogen",
                "number": 1,
                "info": "The lightest and most abundant element in the universe. Essential for water and organic compounds."
            },
            {
                "symbol": "He",
                "name": "Helium",
                "number": 2,
                "info": "A noble gas that is lighter than air. Used in balloons and as a coolant for superconducting magnets."
            }
        ]
        
        for element_data in sample_elements:
            add_element(**element_data)
        
        print("🎉 Sample data initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")
        raise e
    finally:
        db.close()

def create_admin_user(username: str = "admin", password: str = "admin123", role: str = "admin"):
    """
    Create an admin user for testing and initial setup
    
    Args:
        username (str): Admin username (default: "admin")
        password (str): Admin password (default: "admin123")
        role (str): User role (default: "admin")
    
    Returns:
        User: The created admin user
    """
    from passlib.context import CryptContext
    
    # Create password context for hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == username).first()
        if existing_admin:
            print(f"👤 Admin user '{username}' already exists")
            return existing_admin
        
        # Create new admin user
        admin_user = User(
            username=username,
            password_hash=pwd_context.hash(password),
            role=role
        )
        
        # Add to database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Created admin user: {username} (role: {role})")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Role: {role}")
        return admin_user
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
        raise e
    finally:
        db.close()
