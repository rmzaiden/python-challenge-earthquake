import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from helper.database import Base
from models.db.city_model import City
from models.schemas.city_schema import CityCreate
from models.db.state_model import State
from models.db.country_model import Country
from services.city_service import CityService

class TestCityService(unittest.TestCase):
    """
    Unit tests for the CityService class.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        
        country = Country(name="Test Country")
        cls.session.add(country)
        cls.session.commit()
        
        state = State(name="Test State", state_abbreviation="TS", country_id=country.id)
        cls.session.add(state)
        cls.session.commit()

    def test_create_city_success(self):
        """
        Scenario: Create a city successfully.
        """
        # Arrange
        city_service = CityService(session=self.session)
        city_create = CityCreate(name="New City", state_province_id=1)

        # Act
        created_city = city_service.create_city(city_create)

        # Assert
        self.assertIsNotNone(created_city.id)
        self.assertEqual(created_city.name, "New City")

    @patch('sqlalchemy.orm.Session.add')
    def test_create_city_integrity_error(self, mock_add):
        """
        Scenario: An IntegrityError occurs when creating a city trying to insert a duplicate record.
        """
        # Arrange
        city_service = CityService(session=self.session)
        city_create = CityCreate(name="New City", state_province_id=1)
        error_message = "duplicate key value violates unique constraint"
        mock_add.side_effect = IntegrityError("statement", "params", error_message)

        # Act
        with self.assertRaises(ValueError) as context:
            city_service.create_city(city_create)

        # Assert
        self.assertIn("Cannot create city", str(context.exception))
        mock_add.assert_called_once()

    def test_get_city_by_id_success(self):
        """
        Scenario: Get a city by ID successfully.
        """
        with patch('services.city_service.CityService.get_city_by_id') as mock_get_city_by_id:
            # Arrange
            expected_city = MagicMock()
            expected_city.id = 1
            expected_city.name = "Test City"
            mock_get_city_by_id.return_value = expected_city

            # Act
            city_service = CityService()
            city = city_service.get_city_by_id(1)

            # Assert
            mock_get_city_by_id.assert_called_once_with(1)
            assert city.name == "Test City", "City name should match the expected value"

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        Base.metadata.drop_all(cls.engine)   

