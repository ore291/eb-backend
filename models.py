from enum import Enum, IntEnum

from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class UserType(IntEnum):
    admin = 1
    blurber = 2
    client = 3


class Gender(IntEnum):
    not_specified = 1
    male = 2
    female = 3


class AgeBrackets(IntEnum):
    young_adult = 1
    middle_age = 2
    adult = 3


class SalaryRange(IntEnum):
    low = 1
    middle = 2
    high = 3


class EmploymentType(IntEnum):
    unemployed = 1
    self_employed = 2
    employed = 3


class EducationLevel(IntEnum):
    uneducated = 1
    primary_school = 2
    ssce = 3
    nd_hnd = 4
    bsc = 5
    masters = 6
    phd = 7


class WhatsappViews(IntEnum):
    low = 1
    middle = 2
    high = 3


class SocialClass(IntEnum):
    low = 1
    middle = 2
    high = 3



class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)

class State(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name




class Lga(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255)
    state =  fields.ForeignKeyField('models.State', related_name='lgas')

    def __str__(self):
        return self.name


class User(Model):
    id = fields.IntField(pk=True, index=True)
    user_type = fields.IntEnumField(enum_type=UserType, default=UserType.blurber)
    email = fields.CharField(max_length=128, unique=True)
    phone = fields.CharField(max_length=11, null=False)
    username = fields.CharField(
        max_length=128, unique=True, null=True, )
    is_active = fields.BooleanField(null=False, default=True)
    is_verified = fields.BooleanField(null=False, default=False)
    password_hash = fields.CharField(max_length=255, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # class PydanticMeta:
    #    computed = ("password",)
      
       


class Blurb(Model):
    id = fields.IntField(pk=True, indexed=True)
    user = fields.ForeignKeyField('models.User', related_name='blurber')
    no_of_contacts = fields.IntField(null=True, default=0)
    age_bracket = fields.IntEnumField(AgeBrackets, default=AgeBrackets.adult)
    salary_range = fields.IntEnumField(SalaryRange, default=SalaryRange.low)
    employment_type = fields.IntEnumField(
        EmploymentType, default=EmploymentType.self_employed)
    occupation = fields.CharField(max_length=255, null=True, blank=True)
    education_level = fields.IntEnumField(
        EducationLevel, default=EducationLevel.primary_school)
    average_whatsapp_views = fields.IntEnumField(
        WhatsappViews, default=WhatsappViews.low)
    male_viewership = fields.IntField(null=True, default=0)
    female_viewership = fields.IntField(null=True, default=0)
    social_class_viewership = fields.IntEnumField(
        SocialClass, default=SocialClass.middle)
    state_capacities = fields.CharField(max_length=255, null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    first_name = fields.CharField(max_length=50, null=False)
    last_name = fields.CharField(max_length=50, null=False)
    city = fields.CharField(max_length=255, null=True)
    lga = fields.ForeignKeyField('models.Lga', related_name='lga')
    state = fields.ForeignKeyField(
        'models.State', related_name='state')
    gender = fields.IntEnumField(Gender, default=Gender.not_specified)
    bank_name = fields.CharField(128, null=True)
    account_number = fields.CharField(10, null=True)
    account_name = fields.CharField(max_length=255, null=True)

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.first_name


class Client(Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='client')
    company_name = fields.CharField(
        max_length=255, unique=True, null=True, blank=True)
    city = fields.CharField(max_length=255, city="Unspecified", null=True)
    phone = fields.CharField(max_length=11, null=True)
    rep_name = fields.CharField(max_length=255, null=True, blank=True)
    rep_contact = fields.CharField(max_length=255, null=True, blank=True)
    rep_email = fields.CharField(max_length=128, unique=True, null=False)
    company_logo = fields.CharField(max_length=255, default="default.jpg")
    blurb_angel_id = fields.IntField(null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)



user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "is_active",'password_hash' ))
user_pydanticCreate =  pydantic_model_creator(User, name="UserIn", exclude=("is_verified", "is_active","id" ))
user_pydanticOut = pydantic_model_creator(User, name="UserOut",exclude=("password_hash"))


lgaIn = pydantic_model_creator(Lga, name="lgaIn", exclude_readonly=True)


client_pydantic = pydantic_model_creator(Client, name="Client")
client_pydanticCreate = pydantic_model_creator(Client, name="ClientIn", exclude_readonly=True)

blurb_pydantic = pydantic_model_creator(Blurb, name="Blurb")
blurb_pydanticCreate = pydantic_model_creator(Blurb, name="BlurbIn", exclude_readonly=True)
