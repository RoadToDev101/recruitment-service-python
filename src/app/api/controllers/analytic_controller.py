from app.api.schemas.analytic_schema import (
    InputTimeFrame,
    OverallStatistic,
    SuitableSeekers,
)
from app.utils.utils import remove_private_attributes, extract_ids
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.models.employer_model import Employer as EmployerModel
from app.api.models.job_model import Job as JobModel
from app.api.models.seeker_model import Seeker as SeekerModel
from app.api.models.resume_model import Resume as ResumeModel
from app.api.models.job_field_model import JobField as JobFieldModel
from app.api.models.province_model import Province as ProvinceModel
from app.api.schemas.seeker_schema import SeekerOut
from app.common.custom_exception import (
    BadRequestException,
    ValidationException,
    NotFoundException,
)
from datetime import timedelta, date
from pydantic import ValidationError
from collections import defaultdict


input_time_frame = InputTimeFrame(fromDate=date(2022, 1, 1), toDate=date(2022, 12, 31))


class AnalyticController:
    @staticmethod
    def get_overall_statistic(
        db: Session,
        fromDate: date = input_time_frame.fromDate,
        toDate: date = input_time_frame.toDate,
    ) -> OverallStatistic:
        try:
            # Create chart data
            chart = defaultdict(
                lambda: {"numEmployer": 0, "numJob": 0, "numSeeker": 0, "numResume": 0}
            )
            delta = toDate - fromDate
            for i in range(delta.days + 1):
                date = fromDate + timedelta(days=i)
                chart[date]  # Initialize the date in the chart

            # Query all models at once
            for model, key in [
                (EmployerModel, "numEmployer"),
                (JobModel, "numJob"),
                (SeekerModel, "numSeeker"),
                (ResumeModel, "numResume"),
            ]:
                records = (
                    db.query(model)
                    .filter(
                        model.created_at >= fromDate,
                        model.created_at <= toDate,
                    )
                    .all()
                )

                # Update the chart and count the records
                for record in records:
                    chart[record.created_at.date()][key] += 1

            # Convert the chart to a list and sort it by date
            chart = [{"date": date, **data} for date, data in sorted(chart.items())]

            # Create overall statistic
            overall_statistic = OverallStatistic(
                numEmployer=sum(data["numEmployer"] for data in chart),
                numJob=sum(data["numJob"] for data in chart),
                numSeeker=sum(data["numSeeker"] for data in chart),
                numResume=sum(data["numResume"] for data in chart),
                chart=chart,
            )
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting overall statistic. Error: {e}"
            )
        except ValidationError as e:
            raise ValidationException(f"Error validating overall statistic. Error: {e}")

        return overall_statistic

    @staticmethod
    def find_suitable_seekers(db: Session, job_id: int) -> SuitableSeekers:
        try:
            db_job = db.query(JobModel).get(job_id)
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while getting job. Error: {e}")

        if not db_job:
            raise NotFoundException(detail="Job not found")

        try:
            # Get all fields and provinces of the job
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

            # The list is arranged in descending order of expiredAt of the job.

            # Seekers will match jobs if the seeker has a resume that meets the following conditions:
            # 1.Resume whose salary is less than or equal to the salary of the job
            # 2.The resume has 1 field located in the Job's fields
            # 3.The resume has 1 province located in the provinces of the job

            # Query resumes that meet the salary condition
            resumes = (
                db.query(ResumeModel)
                .filter(
                    ResumeModel.salary <= db_job.salary,
                )
                .all()
            )

            # Filter resumes that meet the fields and provinces conditions
            filtered_resumes = [
                resume
                for resume in resumes
                if any(
                    field_id in extract_ids(resume.fields)
                    for field_id in job_field_db_ids
                )
                and any(
                    province_id in extract_ids(resume.provinces)
                    for province_id in job_province_db_ids
                )
            ]

            # Get all seekers from the resumes
            seeker_ids = [resume.seeker_id for resume in filtered_resumes]

            # Remove duplicate seekers
            seeker_ids = list(set(seeker_ids))
            # Find Seekers
            seekers_out = (
                db.query(SeekerModel).filter(SeekerModel.id.in_(seeker_ids)).all()
            )

            seekers = []
            for seeker in seekers_out:
                seeker_dict = remove_private_attributes(seeker)
                seeker_dict["provinceId"] = (
                    seeker.province_data.id if seeker.province_data else None
                )
                seeker_dict["provinceName"] = (
                    seeker.province_data.name if seeker.province_data else None
                )
                seeker_out = SeekerOut.model_validate(seeker_dict)
                seekers.append(seeker_out)

            job_dict = remove_private_attributes(db_job)
            employer = db.query(EmployerModel).get(job_dict["employer_id"])
            if employer:
                job_dict["employerId"] = employer.id
                job_dict["employerName"] = employer.name
            job_dict["seekers"] = seekers
            job_dict["fields"] = job_fields_dict
            job_dict["provinces"] = job_provinces_dict
            suitable_seekers = SuitableSeekers.model_validate(job_dict)
        except SQLAlchemyError as e:
            raise BadRequestException(
                f"Database error while getting suitable seekers. Error: {e}"
            )
        except ValidationError as e:
            raise ValidationException(f"Error validating suitable seekers. Error: {e}")

        return suitable_seekers
