from pydantic import BaseModel, EmailStr
from models import UserType, AgeBrackets, SalaryRange, EmploymentType, EducationLevel, WhatsappViews, SocialClass, Gender
from datetime import datetime
from fastapi import Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

class User(BaseModel):
    email : EmailStr
    phone : str


class UserOut(User):
    username : str
    

class UserBlurbIn(User):
    user_type : UserType = UserType.blurber
    password : str 
    no_of_contacts : int = 0
    age_bracket : AgeBrackets = AgeBrackets.adult
    salary_range : SalaryRange = SalaryRange.low
    employment_type : EmploymentType = EmploymentType.self_employed
    occupation : str = None
    education_level : EducationLevel =EducationLevel.primary_school
    average_whatsapp_views : WhatsappViews = WhatsappViews.low
    male_viewership : int = None
    female_viewership : int = None
    social_class_viewership : SocialClass = SocialClass.middle
    state_capacities : str = None
    first_name : str 
    last_name : str
    city : str = None
    lga_id : int = 1
    state_id : int = 1
    gender : Gender = Gender.not_specified
    bank_name : str = None
    account_number : str = None
    account_name : str = None

    


class UserClientIn(User):
    user_type : UserType = UserType.client
    password : str
    company_name : str = None
    city : str = "Unspecified"
    rep_name : str = None
    rep_contact : str = None
    rep_email : str = None
    company_logo : str = "default.jpg"
    blurb_angel_id : int = None





class UserOut(User):
    created_at : datetime
    updated_at : datetime