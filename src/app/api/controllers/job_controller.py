from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.models.job_model import Job as JobModel
from app.api.schemas.job_schema import JobCreate, JobOut, JobUpdate
from app.api.models.employer_model import Employer as EmployerModel
from app.api.models.job_field_model import JobField as JobFieldModel
from app.api.models.province_model import Province as ProvinceModel
from app.common.custom_exception import (
    NotFoundException,
    BadRequestException,
    ValidationException,
)
from app.common.pagination import Pagination
from app.utils.utils import (
    remove_private_attributes,
    extract_ids,
    format_str_ids,
)


class JobController:
    @staticmethod
    def create_job(db: Session, job: JobCreate) -> str:
        db_employer = db.query(EmployerModel).get(job.employerId)

        if not db_employer:
            raise NotFoundException(detail="Employer not found")

        db_fields = (
            db.query(JobFieldModel).filter(JobFieldModel.id.in_(job.fieldIds)).all()
        )

        if not db_fields:
            raise NotFoundException(detail="Field not found")

        db_provinces = (
            db.query(ProvinceModel).filter(ProvinceModel.id.in_(job.provinceIds)).all()
        )

        if not db_provinces:
            raise NotFoundException(detail="Province not found")

        try:
            new_job = JobModel(
                employer_id=job.employerId,
                title=job.title,
                quantity=job.quantity,
                description=job.description,
                salary=job.salary,
                fields=format_str_ids(job.fieldIds),
                provinces=format_str_ids(job.provinceIds),
                expired_at=job.expiredAt,
            )

            db.add(new_job)

            db.commit()
            db.refresh(new_job)
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while creating job. Error: {e}")
        except ValidationException as e:
            raise ValidationException(f"Error validating job data. Error: {e}")

        return "Job created successfully"

    @staticmethod
    def get_job_by_id(db: Session, job_id: int) -> JobOut:
        try:
            db_job = db.query(JobModel).get(job_id)

            if not db_job:
                raise NotFoundException(detail="Job not found")

            job_dict = remove_private_attributes(db_job)

            employer = db.query(EmployerModel).get(job_dict["employer_id"])
            if employer:
                job_dict["employerId"] = employer.id
                job_dict["employerName"] = employer.name

            job_dict["expiredAt"] = job_dict["expired_at"]

            job_field_db_ids = extract_ids(db_job.fields)
            job_province_db_ids = extract_ids(db_job.provinces)

            db_job_fields = (
                db.query(JobFieldModel)
                .filter(JobFieldModel.id.in_(job_field_db_ids))
                .all()
            )
            db_job_provinces = (
                db.query(ProvinceModel)
                .filter(ProvinceModel.id.in_(job_province_db_ids))
                .all()
            )

            job_fields_dict = [
                remove_private_attributes(field) for field in db_job_fields
            ]
            job_provinces_dict = [
                remove_private_attributes(province) for province in db_job_provinces
            ]

            job_dict["fields"] = job_fields_dict
            job_dict["provinces"] = job_provinces_dict

            job_out = JobOut.model_validate(job_dict)

        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while getting job. Error: {e}")

        return job_out

    @staticmethod
    def get_jobs(db: Session, skip: int = 0, limit: int = 10) -> Pagination[JobOut]:
        try:
            jobs = db.query(JobModel).offset(skip).limit(limit).all()
            total_jobs = db.query(JobModel).count()
            jobs_out = []
            for job in jobs:
                job_dict = remove_private_attributes(job)
                employer = db.query(EmployerModel).get(job_dict["employer_id"])
                if employer:
                    job_dict["employerId"] = employer.id
                    job_dict["employerName"] = employer.name

                job_dict["expiredAt"] = job_dict["expired_at"]

                job_field_db_ids = extract_ids(job.fields)
                job_province_db_ids = extract_ids(job.provinces)

                db_job_fields = (
                    db.query(JobFieldModel)
                    .filter(JobFieldModel.id.in_(job_field_db_ids))
                    .all()
                )
                db_job_provinces = (
                    db.query(ProvinceModel)
                    .filter(ProvinceModel.id.in_(job_province_db_ids))
                    .all()
                )

                job_fields_dict = [
                    remove_private_attributes(field) for field in db_job_fields
                ]
                job_provinces_dict = [
                    remove_private_attributes(province) for province in db_job_provinces
                ]

                job_dict["fields"] = job_fields_dict
                job_dict["provinces"] = job_provinces_dict

                job_out = JobOut.model_validate(job_dict)
                jobs_out.append(job_out)

            result = Pagination[JobOut].create(jobs_out, skip, limit, total_jobs)
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while getting jobs. Error: {e}")
        except ValidationException as e:
            raise ValidationException(f"Error validating job data. Error: {e}")

        return result

    @staticmethod
    def update_job_by_id(db: Session, job_id: int, job: JobUpdate) -> str:
        db_job = db.query(JobModel).get(job_id)

        if not db_job:
            raise NotFoundException(detail="Job not found")

        job_dict = remove_private_attributes(db_job)

        db_employer = db.query(EmployerModel).get(job_dict["employer_id"])

        if not db_employer:
            raise NotFoundException(detail="Employer not found")

        job_field_db_ids = extract_ids(db_job.fields)
        job_province_db_ids = extract_ids(db_job.provinces)

        db_job_fields = (
            db.query(JobFieldModel).filter(JobFieldModel.id.in_(job_field_db_ids)).all()
        )
        db_job_provinces = (
            db.query(ProvinceModel)
            .filter(ProvinceModel.id.in_(job_province_db_ids))
            .all()
        )

        if not db_job_fields:
            raise NotFoundException(detail="Field not found")

        if not db_job_provinces:
            raise NotFoundException(detail="Province not found")

        try:
            db_job.title = job.title
            db_job.quantity = job.quantity
            db_job.description = job.description
            db_job.salary = job.salary
            db_job.fields = format_str_ids(job.fieldIds)
            db_job.provinces = format_str_ids(job.provinceIds)
            db_job.expired_at = job.expiredAt

            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while updating job. Error: {e}")
        except ValidationException as e:
            raise ValidationException(f"Error validating job data. Error: {e}")

        return "Job updated successfully"

    @staticmethod
    def delete_job_by_id(db: Session, job_id: int) -> str:
        db_job = db.query(JobModel).get(job_id)

        if not db_job:
            raise NotFoundException(detail="Job not found")

        try:
            db.delete(db_job)
            db.commit()
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while deleting job. Error: {e}")

        return "Job deleted successfully"
