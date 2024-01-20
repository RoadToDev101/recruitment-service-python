from app.api.models.employer_model import (
    EmployerCreate,
    EmployerUpdate,
    EmployerOut,
    Employer as EmployerModel,
)
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.api.models.province_model import Province as ProvinceModel
from app.common.custom_exception import (
    NotFoundException,
    BadRequestException,
    ValidationException,
)
from app.utils.utils import remove_private_attributes
from app.common.pagination import Pagination


class EmployerController:
    @staticmethod
    def create_employer(db: Session, employer: EmployerCreate) -> str:
        # Check if email already exists
        db_employer = db.query(EmployerModel).filter_by(email=employer.email).first()

        if db_employer:
            raise BadRequestException(detail="Email already exists")

        # Check if province exists
        db_province = db.query(ProvinceModel).get(employer.provinceId)

        if not db_province:
            raise NotFoundException(detail="Province not found")

        try:
            # Create employer
            new_employer = EmployerModel(
                email=employer.email,
                name=employer.name,
                province=employer.provinceId,
                description=employer.description,
            )

            db.add(new_employer)
            db.commit()
            db.refresh(new_employer)
        except IntegrityError:
            raise BadRequestException("Employer already exists")
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while creating employer. Error: {e}"
            )
        except ValidationException as e:
            raise BadRequestException(f"Error validating employer data. Error: {e}")

        return "Employer created successfully"

    @staticmethod
    def get_employer_by_id(db: Session, employer_id: int) -> EmployerOut:
        try:
            db_employer = (
                db.query(EmployerModel)
                .options(
                    joinedload(EmployerModel.province_data)
                )  # Use the relationship name
                .get(employer_id)
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting employer. Error: {e}"
            )

        if not db_employer:
            raise NotFoundException(detail="Employer not found")

        try:
            employer_dict = remove_private_attributes(db_employer)
            employer_dict["provinceId"] = (
                db_employer.province_data.id if db_employer.province_data else None
            )
            employer_dict["provinceName"] = (
                db_employer.province_data.name if db_employer.province_data else None
            )
            employer_out = EmployerOut.model_validate(employer_dict)
        except ValidationException as e:
            raise BadRequestException(f"Error validating employer data. Error: {e}")

        return employer_out

    @staticmethod
    def get_employers(
        db: Session, skip: int = 0, limit: int = 10
    ) -> Pagination[EmployerOut]:
        try:
            employers = db.query(EmployerModel).offset(skip).limit(limit).all()
            total_employers = db.query(EmployerModel).count()
            employers_out = []
            for employer in employers:
                employer_dict = remove_private_attributes(employer)
                employer_dict["provinceId"] = (
                    employer.province_data.id if employer.province_data else None
                )
                employer_dict["provinceName"] = (
                    employer.province_data.name if employer.province_data else None
                )
                employer_out = EmployerOut.model_validate(employer_dict)
                employers_out.append(employer_out)

            result = Pagination[EmployerOut].create(
                employers_out, skip, limit, total_employers
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting employers. Error: {e}"
            )
        except ValidationException as e:
            raise BadRequestException(f"Error validating employer data. Error: {e}")

        return result

    @staticmethod
    def update_employer_by_id(
        db: Session, employer_id: int, employer: EmployerUpdate
    ) -> str:
        try:
            db_employer = db.query(EmployerModel).get(employer_id)

            if not db_employer:
                raise NotFoundException(detail="Employer not found")

            db_employer.name = employer.name
            db_employer.province = employer.provinceId
            db_employer.description = employer.description

            db.commit()
            db.refresh(db_employer)
        except IntegrityError:
            raise BadRequestException("Employer already exists")
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while updating employer. Error: {e}"
            )
        except ValidationException as e:
            raise BadRequestException(f"Error validating employer data. Error: {e}")

        return "Employer updated successfully"

    @staticmethod
    def delete_employer_by_id(db: Session, employer_id: int) -> str:
        db_employer = db.query(EmployerModel).get(employer_id)

        if not db_employer:
            raise NotFoundException(detail="Employer not found")

        try:
            db.delete(db_employer)
            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while deleting employer. Error: {e}"
            )

        return "Employer deleted successfully"
