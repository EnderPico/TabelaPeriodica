"""
Authentication System Tests

This module tests the authentication system including:
- User registration (POST /register)
- User login (POST /login)
- JWT token creation and validation
- Password hashing and verification
- Protected route access
"""

import pytest
from fastapi import status
from jose import jwt
from auth import verify_password, get_password_hash, create_access_token, verify_token

class TestUserRegistration:
    """Test POST /register endpoint"""
    
    def test_register_user_success(self, client, user_registration_data):
        """Test successful user registration"""
        response = client.post("/register", json=user_registration_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["message"] == "User 'testuser' registered successfully"
        assert data["user"]["username"] == "testuser"
        assert data["user"]["role"] == "student"
        assert "id" in data["user"]
        assert "password" not in data["user"]  # Password should not be returned
    
    def test_register_user_default_role(self, client):
        """Test user registration with default role"""
        user_data = {
            "username": "testuser",
            "password": "password123"
            # No role specified, should default to "student"
        }
        
        response = client.post("/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user"]["role"] == "student"
    
    def test_register_user_admin_role(self, client):
        """Test user registration with admin role"""
        user_data = {
            "username": "testadmin",
            "password": "password123",
            "role": "admin"
        }
        
        response = client.post("/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user"]["role"] == "admin"
    
    def test_register_duplicate_username(self, client, admin_user):
        """Test registration with duplicate username"""
        user_data = {
            "username": "admin",  # Already exists
            "password": "password123",
            "role": "student"
        }
        
        response = client.post("/register", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "already registered" in data["detail"].lower()
    
    def test_register_invalid_data(self, client, invalid_user_data):
        """Test registration with invalid data"""
        response = client.post("/register", json=invalid_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data
    
    def test_register_username_validation(self, client):
        """Test username validation"""
        invalid_data = {
            "username": "ab",  # Too short
            "password": "password123",
            "role": "student"
        }
        
        response = client.post("/register", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_password_validation(self, client):
        """Test password validation"""
        invalid_data = {
            "username": "testuser",
            "password": "123",  # Too short
            "role": "student"
        }
        
        response = client.post("/register", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_role_validation(self, client):
        """Test role validation"""
        invalid_data = {
            "username": "testuser",
            "password": "password123",
            "role": "invalid_role"
        }
        
        response = client.post("/register", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestUserLogin:
    """Test POST /login endpoint"""
    
    def test_login_success(self, client, admin_user, login_data):
        """Test successful login"""
        response = client.post("/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["message"] == "Login successful for user 'admin'"
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800  # 30 minutes in seconds
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"
        assert "id" in data["user"]
    
    def test_login_invalid_username(self, client, admin_user):
        """Test login with invalid username"""
        login_data = {
            "username": "nonexistent",
            "password": "admin123"
        }
        
        response = client.post("/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "invalid username or password" in data["detail"].lower()
    
    def test_login_invalid_password(self, client, admin_user, invalid_login_data):
        """Test login with invalid password"""
        response = client.post("/login", json=invalid_login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "invalid username or password" in data["detail"].lower()
    
    def test_login_missing_credentials(self, client, admin_user):
        """Test login with missing credentials"""
        response = client.post("/login", json={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_empty_username(self, client, admin_user):
        """Test login with empty username"""
        login_data = {
            "username": "",
            "password": "admin123"
        }
        
        response = client.post("/login", json=login_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_empty_password(self, client, admin_user):
        """Test login with empty password"""
        login_data = {
            "username": "admin",
            "password": ""
        }
        
        response = client.post("/login", json=login_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestJWTToken:
    """Test JWT token functionality"""
    
    def test_token_creation(self, client, admin_user, login_data):
        """Test JWT token creation"""
        response = client.post("/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        token = data["access_token"]
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are typically long
    
    def test_token_validation(self, client, admin_user, login_data):
        """Test JWT token validation"""
        response = client.post("/login", json=login_data)
        token = response.json()["access_token"]
        
        # Token should be valid
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "admin"
    
    def test_token_invalid(self):
        """Test invalid JWT token"""
        invalid_token = "invalid.token.here"
        
        payload = verify_token(invalid_token)
        assert payload is None
    
    def test_token_expiration(self):
        """Test JWT token expiration"""
        from datetime import timedelta
        
        # Create token with very short expiration
        token = create_access_token(
            data={"sub": "testuser"},
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        payload = verify_token(token)
        assert payload is None
    
    def test_token_structure(self, client, admin_user, login_data):
        """Test JWT token structure"""
        response = client.post("/login", json=login_data)
        token = response.json()["access_token"]
        
        # JWT tokens have 3 parts separated by dots
        parts = token.split(".")
        assert len(parts) == 3
        
        # Each part should be base64 encoded
        for part in parts:
            assert len(part) > 0

class TestPasswordHashing:
    """Test password hashing functionality"""
    
    def test_password_hash_creation(self):
        """Test password hash creation"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 20
    
    def test_password_verification_success(self):
        """Test successful password verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed)
    
    def test_password_verification_failure(self):
        """Test failed password verification"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert not verify_password(wrong_password, hashed)
    
    def test_password_hash_uniqueness(self):
        """Test that same password produces different hashes"""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Different hashes due to salt
        assert hash1 != hash2
        
        # But both should verify the same password
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)

class TestProtectedRoutes:
    """Test access to protected routes"""
    
    def test_protected_route_without_token(self, client, sample_element_data):
        """Test accessing protected route without token"""
        response = client.post("/elements", json=sample_element_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "not authenticated" in data["detail"].lower()
    
    def test_protected_route_with_invalid_token(self, client, sample_element_data):
        """Test accessing protected route with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/elements", json=sample_element_data, headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "could not validate credentials" in data["detail"].lower()
    
    def test_protected_route_with_valid_token(self, client, admin_headers, sample_element_data):
        """Test accessing protected route with valid token"""
        response = client.post("/elements", json=sample_element_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_protected_route_malformed_token(self, client, sample_element_data):
        """Test accessing protected route with malformed token"""
        headers = {"Authorization": "Bearer"}
        response = client.post("/elements", json=sample_element_data, headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_protected_route_wrong_auth_type(self, client, sample_element_data):
        """Test accessing protected route with wrong auth type"""
        headers = {"Authorization": "Basic dXNlcjpwYXNz"}
        response = client.post("/elements", json=sample_element_data, headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

class TestTokenRefresh:
    """Test token refresh scenarios"""
    
    def test_token_reuse(self, client, admin_user, login_data):
        """Test that same token can be reused multiple times"""
        # Login to get token
        response = client.post("/login", json=login_data)
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Use token multiple times
        for _ in range(3):
            response = client.get("/elements", headers=headers)
            assert response.status_code == status.HTTP_200_OK
    
    def test_token_after_user_deletion(self, client, test_db, admin_user):
        """Test token behavior after user is deleted"""
        # Login to get token
        login_data = {"username": "admin", "password": "admin123"}
        response = client.post("/login", json=login_data)
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Delete user from database
        test_db.delete(admin_user)
        test_db.commit()
        
        # Token should still work (no immediate invalidation)
        response = client.get("/elements", headers=headers)
        assert response.status_code == status.HTTP_200_OK
