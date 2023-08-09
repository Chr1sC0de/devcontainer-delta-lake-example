from collections import OrderedDict

from testlib.settings import config

model = OrderedDict()


model[
    "university-bronze"
] = f"""
create database if not exists university
    location '{config.s3_path_bronze_university}'
"""

model[
    "students"
] = f"""
    create table if not exists university.students (
        id long,
        first_name string, 
        last_name string
    )
    using delta
    location '{config.s3_path_bronze_university}/students'
"""


model[
    "courses"
] = f"""
    create table if not exists university.courses (
        id long,
        code string, 
        name string
    )
    using delta
    location '{config.s3_path_bronze_university}/courses'
"""

model[
    "semesters"
] = f"""
    create table if not exists university.terms (
        id short,
        name string,
        start_date date,
        end_date date
    )
    using delta
    location '{config.s3_path_bronze_university}/terms'
"""

model[
    "enrolments"
] = f"""
    create table if not exists university.enrollments (
        id int,
        student_id int,
        course_id int,
        term_id int
    )
    using delta
    location '{config.s3_path_bronze_university}/enrollments'
"""
