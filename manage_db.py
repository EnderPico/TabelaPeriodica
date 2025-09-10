"""
Database Management Script for Periodic Table Web App
Helper script to manage the SQLite database and add elements

This script provides easy functions to add elements to the database
without needing to modify the main application code
"""

from models import add_element, create_tables, init_sample_data, SessionLocal, Element

def add_sample_elements():
    """
    Add more sample elements to the database
    
    This function demonstrates how to add elements using the add_element helper function
    You can modify this function to add more elements as you research them
    """
    print("🔬 Adding sample elements to database...")
    
    # Example elements - you can add more here
    sample_elements = [
        {
            "symbol": "Li",
            "name": "Lithium",
            "number": 3,
            "info": "The lightest metal. Used in batteries and psychiatric medications."
        },
        {
            "symbol": "C",
            "name": "Carbon",
            "number": 6,
            "info": "The basis of all organic life. Forms millions of compounds and is essential for life on Earth."
        },
        {
            "symbol": "N",
            "name": "Nitrogen",
            "number": 7,
            "info": "Makes up 78% of Earth's atmosphere. Essential for proteins and DNA."
        },
        {
            "symbol": "O",
            "name": "Oxygen",
            "number": 8,
            "info": "Essential for respiration and combustion. Makes up about 21% of Earth's atmosphere."
        },
        {
            "symbol": "F",
            "name": "Fluorine",
            "number": 9,
            "info": "The most reactive element. Used in toothpaste and non-stick coatings."
        }
    ]
    
    for element_data in sample_elements:
        try:
            add_element(**element_data)
        except Exception as e:
            print(f"⚠️  Could not add {element_data['symbol']}: {e}")
    
    print("✅ Sample elements added!")

def list_all_elements():
    """
    List all elements currently in the database
    """
    db = SessionLocal()
    try:
        elements = db.query(Element).all()
        print(f"\n📋 Found {len(elements)} elements in database:")
        print("-" * 50)
        
        for element in elements:
            print(f"{element.number:2d}. {element.symbol:2s} - {element.name:12s} | {element.info[:50]}...")
        
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error listing elements: {e}")
    finally:
        db.close()

def reset_database():
    """
    Reset the database (delete all data and recreate tables)
    WARNING: This will delete all existing data!
    """
    print("⚠️  WARNING: This will delete all existing data!")
    confirm = input("Are you sure you want to reset the database? (yes/no): ")
    
    if confirm.lower() == "yes":
        import os
        if os.path.exists("periodic_table.db"):
            os.remove("periodic_table.db")
            print("🗑️  Database file deleted")
        
        create_tables()
        init_sample_data()
        print("✅ Database reset complete!")
    else:
        print("❌ Database reset cancelled")

def main():
    """
    Main function - interactive menu for database management
    """
    print("🧪 Periodic Table Database Manager")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Add sample elements")
        print("2. List all elements")
        print("3. Add custom element")
        print("4. Reset database")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            add_sample_elements()
        
        elif choice == "2":
            list_all_elements()
        
        elif choice == "3":
            print("\nAdd custom element:")
            symbol = input("Symbol (e.g., 'Na'): ").strip()
            name = input("Name (e.g., 'Sodium'): ").strip()
            number = input("Atomic number (e.g., '11'): ").strip()
            info = input("Description (optional): ").strip()
            
            try:
                add_element(symbol, name, int(number), info)
            except ValueError:
                print("❌ Invalid atomic number. Please enter a number.")
            except Exception as e:
                print(f"❌ Error adding element: {e}")
        
        elif choice == "4":
            reset_database()
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
