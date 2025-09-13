"""
User Roles and Permissions Tests

This module tests role-based access control (RBAC) functionality:
- Admin users can perform all CRUD operations
- Student users can only read elements (GET operations)
- Unauthenticated users can only read elements
- Role validation and enforcement
"""

import pytest
from fastapi import status

class TestAdminPermissions:
    """Test admin user permissions"""
    
    def test_admin_can_read_elements(self, client, admin_headers, sample_elements):
        """Test that admin can read all elements"""
        response = client.get("/elements", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_admin_can_read_single_element(self, client, admin_headers, sample_elements):
        """Test that admin can read single element"""
        response = client.get("/elements/H", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["symbol"] == "H"
    
    def test_admin_can_create_element(self, client, admin_headers, sample_element_data):
        """Test that admin can create elements"""
        response = client.post("/elements", json=sample_element_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["element"]["symbol"] == "O"
    
    def test_admin_can_update_element(self, client, admin_headers, sample_elements):
        """Test that admin can update elements"""
        update_data = {"info": "Updated by admin"}
        
        response = client.put("/elements/H", json=update_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["element"]["info"] == "Updated by admin"
    
    def test_admin_can_delete_element(self, client, admin_headers, sample_elements):
        """Test that admin can delete elements"""
        response = client.delete("/elements/H", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Element 'H' deleted successfully"
    
    def test_admin_can_access_all_endpoints(self, client, admin_headers, sample_elements, sample_element_data):
        """Test that admin has access to all CRUD endpoints"""
        # GET all elements
        response = client.get("/elements", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # GET single element
        response = client.get("/elements/H", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # POST create element
        response = client.post("/elements", json=sample_element_data, headers=admin_headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        # PUT update element
        update_data = {"info": "Admin update"}
        response = client.put("/elements/H", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # DELETE element
        response = client.delete("/elements/He", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK

class TestStudentPermissions:
    """Test student user permissions"""
    
    def test_student_can_read_elements(self, client, student_headers, sample_elements):
        """Test that student can read all elements"""
        response = client.get("/elements", headers=student_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_student_can_read_single_element(self, client, student_headers, sample_elements):
        """Test that student can read single element"""
        response = client.get("/elements/H", headers=student_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["symbol"] == "H"
    
    def test_student_cannot_create_element(self, client, student_headers, sample_element_data):
        """Test that student cannot create elements"""
        response = client.post("/elements", json=sample_element_data, headers=student_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "not enough permissions" in data["detail"].lower()
        assert "admin role required" in data["detail"].lower()
    
    def test_student_cannot_update_element(self, client, student_headers, sample_elements):
        """Test that student cannot update elements"""
        update_data = {"info": "This should fail"}
        
        response = client.put("/elements/H", json=update_data, headers=student_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "not enough permissions" in data["detail"].lower()
    
    def test_student_cannot_delete_element(self, client, student_headers, sample_elements):
        """Test that student cannot delete elements"""
        response = client.delete("/elements/H", headers=student_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "not enough permissions" in data["detail"].lower()
    
    def test_student_read_only_access(self, client, student_headers, sample_elements):
        """Test that student has read-only access"""
        # Should be able to read
        response = client.get("/elements", headers=student_headers)
        assert response.status_code == status.HTTP_200_OK
        
        response = client.get("/elements/H", headers=student_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Should not be able to modify
        sample_data = {"symbol": "X", "name": "Test", "number": 100, "info": "Test"}
        
        response = client.post("/elements", json=sample_data, headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        response = client.put("/elements/H", json={"info": "Test"}, headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        response = client.delete("/elements/H", headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

class TestUnauthenticatedAccess:
    """Test unauthenticated user access"""
    
    def test_unauthenticated_can_read_elements(self, client, sample_elements):
        """Test that unauthenticated users can read elements"""
        response = client.get("/elements")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_unauthenticated_can_read_single_element(self, client, sample_elements):
        """Test that unauthenticated users can read single element"""
        response = client.get("/elements/H")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["symbol"] == "H"
    
    def test_unauthenticated_cannot_create_element(self, client, sample_element_data):
        """Test that unauthenticated users cannot create elements"""
        response = client.post("/elements", json=sample_element_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "not authenticated" in data["detail"].lower()
    
    def test_unauthenticated_cannot_update_element(self, client, sample_elements):
        """Test that unauthenticated users cannot update elements"""
        update_data = {"info": "This should fail"}
        
        response = client.put("/elements/H", json=update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "not authenticated" in data["detail"].lower()
    
    def test_unauthenticated_cannot_delete_element(self, client, sample_elements):
        """Test that unauthenticated users cannot delete elements"""
        response = client.delete("/elements/H")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "not authenticated" in data["detail"].lower()
    
    def test_unauthenticated_read_only_access(self, client, sample_elements):
        """Test that unauthenticated users have read-only access"""
        # Should be able to read
        response = client.get("/elements")
        assert response.status_code == status.HTTP_200_OK
        
        response = client.get("/elements/H")
        assert response.status_code == status.HTTP_200_OK
        
        # Should not be able to modify
        sample_data = {"symbol": "X", "name": "Test", "number": 100, "info": "Test"}
        
        response = client.post("/elements", json=sample_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        response = client.put("/elements/H", json={"info": "Test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        response = client.delete("/elements/H")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

class TestRoleValidation:
    """Test role validation and enforcement"""
    
    def test_role_case_sensitivity(self, client, test_db):
        """Test that role validation is case-sensitive"""
        # Create user with uppercase role
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "ADMIN"  # Uppercase
        }
        
        response = client.post("/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data
    
    def test_role_validation(self, client):
        """Test role validation"""
        invalid_roles = ["user", "moderator", "guest", "superuser", ""]
        
        for role in invalid_roles:
            user_data = {
                "username": f"testuser_{role}",
                "password": "password123",
                "role": role
            }
            
            response = client.post("/register", json=user_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_valid_roles(self, client):
        """Test that valid roles are accepted"""
        valid_roles = ["admin", "student"]
        
        for i, role in enumerate(valid_roles):
            user_data = {
                "username": f"testuser_{i}",
                "password": "password123",
                "role": role
            }
            
            response = client.post("/register", json=user_data)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["user"]["role"] == role

class TestRoleBasedElementAccess:
    """Test role-based access to specific element operations"""
    
    def test_admin_full_crud_access(self, client, admin_headers, sample_elements):
        """Test admin has full CRUD access to elements"""
        # Create
        new_element = {"symbol": "F", "name": "Fluorine", "number": 9, "info": "Most reactive"}
        response = client.post("/elements", json=new_element, headers=admin_headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Read
        response = client.get("/elements/F", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Update
        update_data = {"info": "Updated by admin"}
        response = client.put("/elements/F", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Delete
        response = client.delete("/elements/F", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
    
    def test_student_read_only_access(self, client, student_headers, sample_elements):
        """Test student has read-only access to elements"""
        # Can read
        response = client.get("/elements", headers=student_headers)
        assert response.status_code == status.HTTP_200_OK
        
        response = client.get("/elements/H", headers=student_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Cannot modify
        new_element = {"symbol": "F", "name": "Fluorine", "number": 9, "info": "Most reactive"}
        
        response = client.post("/elements", json=new_element, headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        response = client.put("/elements/H", json={"info": "Updated"}, headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        response = client.delete("/elements/H", headers=student_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_role_permission_consistency(self, client, admin_headers, student_headers, sample_elements):
        """Test that role permissions are consistent across all operations"""
        # Admin should have consistent access
        admin_operations = [
            ("GET", "/elements"),
            ("GET", "/elements/H"),
            ("POST", "/elements"),
            ("PUT", "/elements/H"),
            ("DELETE", "/elements/He")
        ]
        
        for method, endpoint in admin_operations:
            if method == "GET":
                response = client.get(endpoint, headers=admin_headers)
            elif method == "POST":
                response = client.post(endpoint, json={"symbol": "X", "name": "Test", "number": 100, "info": "Test"}, headers=admin_headers)
            elif method == "PUT":
                response = client.put(endpoint, json={"info": "Test"}, headers=admin_headers)
            elif method == "DELETE":
                response = client.delete(endpoint, headers=admin_headers)
            
            # Admin should have access (200, 201, or 404 for not found)
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND]
        
        # Student should have limited access
        student_read_operations = [
            ("GET", "/elements"),
            ("GET", "/elements/H")
        ]
        
        for method, endpoint in student_read_operations:
            response = client.get(endpoint, headers=student_headers)
            assert response.status_code == status.HTTP_200_OK
        
        student_write_operations = [
            ("POST", "/elements"),
            ("PUT", "/elements/H"),
            ("DELETE", "/elements/H")
        ]
        
        for method, endpoint in student_write_operations:
            if method == "POST":
                response = client.post(endpoint, json={"symbol": "X", "name": "Test", "number": 100, "info": "Test"}, headers=student_headers)
            elif method == "PUT":
                response = client.put(endpoint, json={"info": "Test"}, headers=student_headers)
            elif method == "DELETE":
                response = client.delete(endpoint, headers=student_headers)
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
