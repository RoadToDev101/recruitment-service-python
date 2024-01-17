import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.api.controllers.employer_controller import (
    EmployerController,
    EmployerCreate,
)
from app.api.models.employer_model import Employer as EmployerModel
from app.api.models.province_model import Province as ProvinceModel
from app.common.custom_exception import BadRequestException, NotFoundException


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
