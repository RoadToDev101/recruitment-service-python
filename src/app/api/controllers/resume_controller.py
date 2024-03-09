from src.app.api.models.resume_model import Resume as ResumeModel
from src.app.api.schemas.resume_schema import ResumeCreate, ResumeOut, ResumeUpdate
from src.app.api.models.seeker_model import Seeker as SeekerModel
from src.app.api.models.job_field_model import JobField as JobFieldModel
from src.app.api.models.province_model import Province as ProvinceModel
from src.app.common.custom_exception import (
    NotFoundException,
    BadRequestException,
    ValidationException,
)
from src.app.common.pagination import Pagination
from src.app.utils.utils import (
    remove_private_attributes,
    extract_ids,
    format_str_ids,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class ResumeController:
    @staticmethod
    def create_resume(db: Session, resume: ResumeCreate) -> str:
        db_seeker = db.query(SeekerModel).get(resume.seekerId)

        if not db_seeker:
            raise NotFoundException(detail="Seeker not found")

        db_fields = (
            db.query(JobFieldModel).filter(JobFieldModel.id.in_(resume.fieldIds)).all()
        )

        if not db_fields:
            raise NotFoundException(detail="Field not found")

        db_provinces = (
            db.query(ProvinceModel)
            .filter(ProvinceModel.id.in_(resume.provinceIds))
            .all()
        )

        if not db_provinces:
            raise NotFoundException(detail="Province not found")

        try:
            new_resume = ResumeModel(
                seeker_id=resume.seekerId,
                career_obj=resume.careerObj,
                title=resume.title,
                salary=resume.salary,
                fields=format_str_ids(resume.fieldIds),
                provinces=format_str_ids(resume.provinceIds),
            )

            db.add(new_resume)

            db.commit()
            db.refresh(new_resume)
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while creating resume. Error: {e}"
            )
        except ValidationException as e:
            raise ValidationException(
                f"Validation error while creating resume. Error: {e}"
            )

        return "Resume created successfully"

    @staticmethod
    def get_resume_by_id(db: Session, resume_id: int) -> ResumeOut:
        try:
            db_resume = db.query(ResumeModel).get(resume_id)

            if not db_resume:
                raise NotFoundException(detail="Resume not found")

            resume_dict = remove_private_attributes(db_resume)

            seeker = db.query(SeekerModel).get(resume_dict["seeker_id"])
            if seeker:
                resume_dict["seekerId"] = seeker.id
                resume_dict["seekerName"] = seeker.name

            resume_dict["careerObj"] = resume_dict["career_obj"]

            resume_field_db_ids = extract_ids(db_resume.fields)
            resume_province_db_ids = extract_ids(db_resume.provinces)

            db_resume_fields = (
                db.query(JobFieldModel)
                .filter(JobFieldModel.id.in_(resume_field_db_ids))
                .all()
            )

            db_resume_provinces = (
                db.query(ProvinceModel)
                .filter(ProvinceModel.id.in_(resume_province_db_ids))
                .all()
            )

            resume_fields_dict = [
                remove_private_attributes(field) for field in db_resume_fields
            ]
            resume_provinces_dict = [
                remove_private_attributes(province) for province in db_resume_provinces
            ]

            resume_dict["fields"] = resume_fields_dict
            resume_dict["provinces"] = resume_provinces_dict

            resume_out = ResumeOut.model_validate(resume_dict)

        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting resume. Error: {e}"
            )

        return resume_out

    @staticmethod
    def get_resumes(
        db: Session, skip: int = 0, limit: int = 10
    ) -> Pagination[ResumeOut]:
        try:
            db_resumes = db.query(ResumeModel).offset(skip).limit(limit).all()
            total_resumes = db.query(ResumeModel).count()
            resumes_out = []
            for db_resume in db_resumes:
                resume_dict = remove_private_attributes(db_resume)

                seeker = db.query(SeekerModel).get(resume_dict["seeker_id"])
                if seeker:
                    resume_dict["seekerId"] = seeker.id
                    resume_dict["seekerName"] = seeker.name

                resume_dict["careerObj"] = resume_dict["career_obj"]

                resume_field_db_ids = extract_ids(db_resume.fields)
                resume_province_db_ids = extract_ids(db_resume.provinces)

                db_resume_fields = (
                    db.query(JobFieldModel)
                    .filter(JobFieldModel.id.in_(resume_field_db_ids))
                    .all()
                )

                db_resume_provinces = (
                    db.query(ProvinceModel)
                    .filter(ProvinceModel.id.in_(resume_province_db_ids))
                    .all()
                )

                resume_fields_dict = [
                    remove_private_attributes(field) for field in db_resume_fields
                ]
                resume_provinces_dict = [
                    remove_private_attributes(province)
                    for province in db_resume_provinces
                ]

                resume_dict["fields"] = resume_fields_dict
                resume_dict["provinces"] = resume_provinces_dict

                resume_out = ResumeOut.model_validate(resume_dict)
                resumes_out.append(resume_out)

            result = Pagination[ResumeOut].create(
                resumes_out, skip, limit, total_resumes
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting resume. Error: {e}"
            )
        except ValidationException as e:
            raise ValidationException(
                f"Validation error while getting resume. Error: {e}"
            )

        return result

    @staticmethod
    def update_resume_by_id(db: Session, resume_id: int, resume: ResumeUpdate) -> str:
        db_resume = db.query(ResumeModel).get(resume_id)

        if not db_resume:
            raise NotFoundException(detail="Resume not found")

        resume_dict = remove_private_attributes(db_resume)

        db_seeker = db.query(SeekerModel).get(resume_dict["seeker_id"])

        if not db_seeker:
            raise NotFoundException(detail="Seeker not found")

        job_field_db_ids = extract_ids(db_resume.fields)
        job_province_db_ids = extract_ids(db_resume.provinces)

        db_resume_fields = (
            db.query(JobFieldModel).filter(JobFieldModel.id.in_(job_field_db_ids)).all()
        )

        db_resume_provinces = (
            db.query(ProvinceModel)
            .filter(ProvinceModel.id.in_(job_province_db_ids))
            .all()
        )

        if not db_resume_fields:
            raise NotFoundException(detail="Field not found")

        if not db_resume_provinces:
            raise NotFoundException(detail="Province not found")

        try:
            db_resume.career_obj = resume.careerObj
            db_resume.title = resume.title
            db_resume.salary = resume.salary
            db_resume.fields = format_str_ids(resume.fieldIds)
            db_resume.provinces = format_str_ids(resume.provinceIds)

            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while updating resume. Error: {e}"
            )
        except ValidationException as e:
            raise ValidationException(
                f"Validation error while updating resume. Error: {e}"
            )

        return "Resume updated successfully"

    @staticmethod
    def delete_resume_by_id(db: Session, resume_id: int) -> str:
        db_resume = db.query(ResumeModel).get(resume_id)

        if not db_resume:
            raise NotFoundException(detail="Resume not found")

        try:
            db.delete(db_resume)
            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while deleting resume. Error: {e}"
            )

        return "Resume deleted successfully"
