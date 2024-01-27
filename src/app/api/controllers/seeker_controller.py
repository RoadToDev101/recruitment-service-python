from app.api.models.seeker_model import Seeker as SeekerModel
from app.api.schemas.seeker_schema import SeekerCreate, SeekerOut, SeekerUpdate
from app.api.models.province_model import Province as ProvinceModel
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.common.custom_exception import BadRequestException, NotFoundException
from pydantic import ValidationError
from app.utils.utils import remove_private_attributes
from app.common.pagination import Pagination


class SeekerController:
    @staticmethod
    def create_seeker(db: Session, seeker: SeekerCreate) -> str:
        # Check if province exists
        db_province = db.query(ProvinceModel).get(seeker.provinceId)

        if not db_province:
            raise NotFoundException(detail="Province not found")

        try:
            db_seeker = SeekerModel(
                name=seeker.name,
                birthday=seeker.birthday,
                address=seeker.address,
                province=seeker.provinceId,
            )

            db.add(db_seeker)
            db.commit()
            db.refresh(db_seeker)
        except IntegrityError:
            raise BadRequestException("Seeker already exists")
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while creating seeker. Error: {e}"
            )
        except ValidationError as e:
            raise BadRequestException(f"Error validating seeker data. Error: {e}")

        return "Seeker created successfully"

    @staticmethod
    def get_seeker_by_id(db: Session, seeker_id: int) -> SeekerOut:
        try:
            db_seeker = (
                db.query(SeekerModel)
                .options(joinedload(SeekerModel.province_data))
                .get(seeker_id)
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting seeker. Error: {e}"
            )

        if not db_seeker:
            raise NotFoundException(detail="Seeker not found")

        try:
            seeker_dict = remove_private_attributes(db_seeker)
            seeker_dict["provinceId"] = (
                db_seeker.province_data.id if db_seeker.province_data else None
            )
            seeker_dict["provinceName"] = (
                db_seeker.province_data.name if db_seeker.province_data else None
            )
            seeker_out = SeekerOut.model_validate(seeker_dict)
        except ValidationError as e:
            raise BadRequestException(f"Error validating seeker data. Error: {e}")

        return seeker_out

    @staticmethod
    def get_seekers(
        db: Session, skip: int = 0, limit: int = 100
    ) -> Pagination[SeekerOut]:
        try:
            seekers = db.query(SeekerModel).offset(skip).limit(limit).all()
            total_seekers = db.query(SeekerModel).count()
            seekers_out = []
            for seeker in seekers:
                seeker_dict = remove_private_attributes(seeker)

                seeker_dict["provinceId"] = (
                    seeker.province_data.id if seeker.province_data else None
                )
                seeker_dict["provinceName"] = (
                    seeker.province_data.name if seeker.province_data else None
                )
                seeker_out = SeekerOut.model_validate(seeker_dict)
                seekers_out.append(seeker_out)

            result = Pagination[SeekerOut].create(
                seekers_out, skip, limit, total_seekers
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting seekers. Error: {e}"
            )
        except ValidationError as e:
            raise BadRequestException(f"Error validating seeker data. Error: {e}")

        return result

    @staticmethod
    def update_seeker_by_id(db: Session, seeker_id: int, seeker: SeekerUpdate) -> str:
        try:
            db_seeker = db.query(SeekerModel).get(seeker_id)

            if not db_seeker:
                raise NotFoundException(detail="Seeker not found")

            db_province = db.query(ProvinceModel).get(seeker.provinceId)

            if not db_province:
                raise NotFoundException(detail="Province not found")

            db_seeker.name = seeker.name
            db_seeker.birthday = seeker.birthday
            db_seeker.address = seeker.address
            db_seeker.province = seeker.provinceId

            db.commit()
            db.refresh(db_seeker)
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while updating seeker. Error: {e}"
            )
        except ValidationError as e:
            raise BadRequestException(f"Error validating seeker data. Error: {e}")

        return "Seeker updated successfully"

    @staticmethod
    def delete_seeker_by_id(db: Session, seeker_id: int) -> str:
        db_seeker = db.query(SeekerModel).get(seeker_id)

        if not db_seeker:
            raise NotFoundException(detail="Seeker not found")

        try:
            db.delete(db_seeker)
            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while deleting seeker. Error: {e}"
            )

        return "Seeker deleted successfully"
