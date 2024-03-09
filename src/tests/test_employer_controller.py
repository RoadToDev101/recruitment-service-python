import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.app.api.controllers.employer_controller import (
    EmployerController,
    EmployerCreate,
    EmployerUpdate,
)
from src.app.api.models.employer_model import Employer as EmployerModel
from src.app.api.models.province_model import Province as ProvinceModel
from src.app.common.custom_exception import (
    BadRequestException,
    NotFoundException,
    ValidationException,
)
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import call


class TestEmployerController:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.db = MagicMock(spec=Session)

    def test_create_employer_success(self):
        # Arrange
        employer_data = EmployerCreate(
            email="test@example.com",
            name="Test Employer",
            provinceId=1,
            description="Test description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.filter_by.return_value.first.return_value = None
        self.db.query.return_value.get.return_value = ProvinceModel(id=1)

        # Act
        result = employer_controller.create_employer(self.db, employer_data)

        # Assert
        assert result == "Employer created successfully"
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_create_employer_email_exists(self):
        # Arrange
        employer_data = EmployerCreate(
            email="test@example.com",
            name="Test Employer",
            provinceId=1,
            description="Test description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.filter_by.return_value.first.return_value = (
            EmployerModel()
        )

        # Act & Assert
        with pytest.raises(BadRequestException):
            employer_controller.create_employer(self.db, employer_data)

    def test_create_employer_province_not_found(self):
        # Arrange
        employer_data = EmployerCreate(
            email="test@example.com",
            name="Test Employer",
            provinceId=1,
            description="Test description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.filter_by.return_value.first.return_value = None
        self.db.query.return_value.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            employer_controller.create_employer(self.db, employer_data)

    def test_get_employer_by_id_success(self):
        # Arrange
        employer_id = 1
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.options.return_value.get.return_value = (
            EmployerModel(
                id=1,
                email="test@example.com",
                name="Test Employer",
                province_data=ProvinceModel(id=1, name="Test Province"),
                description="Test description",
            )
        )

        # Act
        result = employer_controller.get_employer_by_id(self.db, employer_id)

        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        assert result.name == "Test Employer"
        assert result.provinceId == 1
        assert result.provinceName == "Test Province"
        assert result.description == "Test description"

    def test_get_employer_by_id_not_found(self):
        # Arrange
        employer_id = 1
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.options.return_value.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            employer_controller.get_employer_by_id(self.db, employer_id)

    def test_get_employer_by_id_exception(self):
        # Arrange
        employer_id = 1
        employer_controller = EmployerController()

        # Mock the query methods to raise a ValidationException
        self.db.query.return_value.options.return_value.get.side_effect = (
            ValidationException("Test exception")
        )

        # Act & Assert
        with pytest.raises(ValidationException):
            employer_controller.get_employer_by_id(self.db, employer_id)

    def test_get_employers_success(self):
        # Arrange
        employer_controller = EmployerController()
        employers = [
            EmployerModel(
                id=i,
                email=f"test{i}@example.com",
                name=f"Test Employer {i}",
                province_data=ProvinceModel(id=i, name=f"Test Province {i}"),
                description=f"Test description {i}",
            )
            for i in range(1, 11)
        ]

        # Mock the query methods
        self.db.query.return_value.offset.return_value.limit.return_value.all.return_value = (
            employers
        )
        self.db.query.return_value.count.return_value = len(employers)

        # Act
        result = employer_controller.get_employers(self.db, skip=0, limit=10)

        # Assert
        assert len(result.data) == 10
        for i in range(10):
            assert result.data[i].id == i + 1
            assert result.data[i].email == f"test{i + 1}@example.com"
            assert result.data[i].name == f"Test Employer {i + 1}"
            assert result.data[i].provinceId == i + 1
            assert result.data[i].provinceName == f"Test Province {i + 1}"
            assert result.data[i].description == f"Test description {i + 1}"
        assert result.pagination.totalElements == 10

    def test_update_employer_by_id_success(self):
        # Arrange
        employer_id = 1
        employer_data = EmployerUpdate(
            name="Updated Employer",
            provinceId=2,
            description="Updated description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = EmployerModel(
            id=employer_id,
            name="Test Employer",
            province_data=ProvinceModel(id=1, name="Test Province"),
            description="Test description",
        )

        # Act
        result = employer_controller.update_employer_by_id(
            self.db, employer_id, employer_data
        )

        # Assert
        assert result == "Employer updated successfully"
        assert self.db.commit.call_count == 1
        assert self.db.refresh.call_count == 1
        assert self.db.query.return_value.get.call_count == 1
        assert self.db.query.return_value.get.call_args == call(employer_id)
        assert self.db.query.return_value.get.return_value.name == "Updated Employer"
        assert self.db.query.return_value.get.return_value.province == 2
        assert (
            self.db.query.return_value.get.return_value.description
            == "Updated description"
        )

    def test_update_employer_by_id_not_found(self):
        # Arrange
        employer_id = 1
        employer_data = EmployerUpdate(
            name="Updated Employer",
            provinceId=2,
            description="Updated description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            employer_controller.update_employer_by_id(
                self.db, employer_id, employer_data
            )

    def test_update_employer_by_id_database_error(self):
        # Arrange
        employer_id = 1
        employer_data = EmployerUpdate(
            name="Updated Employer",
            provinceId=2,
            description="Updated description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = EmployerModel(
            id=employer_id,
            name="Test Employer",
            province_data=ProvinceModel(id=1, name="Test Province"),
            description="Test description",
        )
        self.db.commit.side_effect = SQLAlchemyError()

        # Act & Assert
        with pytest.raises(BadRequestException):
            employer_controller.update_employer_by_id(
                self.db, employer_id, employer_data
            )

    def test_update_employer_by_id_validation_error(self):
        # Arrange
        employer_id = 1
        employer_data = EmployerUpdate(
            name="Updated Employer",
            provinceId=2,
            description="Updated description",
        )
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = EmployerModel(
            id=employer_id,
            name="Test Employer",
            province_data=ProvinceModel(id=1, name="Test Province"),
            description="Test description",
        )
        self.db.commit.side_effect = ValidationException()

        # Act & Assert
        with pytest.raises(BadRequestException):
            employer_controller.update_employer_by_id(
                self.db, employer_id, employer_data
            )

    def test_delete_employer_by_id_success(self):
        # Arrange
        employer_id = 1
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = EmployerModel(id=employer_id)

        # Act
        result = employer_controller.delete_employer_by_id(self.db, employer_id)

        # Assert
        assert result == "Employer deleted successfully"
        self.db.delete.assert_called_once_with(
            self.db.query.return_value.get.return_value
        )
        self.db.commit.assert_called_once()

    def test_delete_employer_by_id_not_found(self):
        # Arrange
        employer_id = 1
        employer_controller = EmployerController()

        # Mock the query methods
        self.db.query.return_value.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            employer_controller.delete_employer_by_id(self.db, employer_id)
