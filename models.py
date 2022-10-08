from enum import Enum, IntEnum

from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model


class UserType(IntEnum):
    admin = 1
    blurber = 2
    client = 3

class TransactionType(IntEnum):
    credit = 1
    debit = 2
   


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
    lgas: fields.ReverseRelation["Lga"]

    class PydanticMeta:
        exclude = ("state", )

    def __str__(self):
        return self.name


class Lga(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255)
    state: fields.ForeignKeyRelation[State] = fields.ForeignKeyField(
        'models.State', related_name='lgas')

    class PydanticMeta:
        exclude = ("lga", )

    def __str__(self):
        return self.name


class User(Model):
    id = fields.IntField(pk=True, index=True)
    user_type = fields.IntEnumField(
        enum_type=UserType, default=UserType.blurber)
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


class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class Product(TimestampMixin, Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255, null=False, unique=True)
    price = fields.BigIntField(default=0)
    blurbers_count = fields.IntField(null=True , default=10)
    price_formatted = fields.CharField(max_length=255, null=True)
    max_file_upload = fields.IntField(default=1)
    overall_imp = fields.IntField(null = False, default=1)
    duration_formatted = fields.CharField(max_length=255,  null = True, default="1 day in a week")
    active_dates = fields.JSONField(null = True, default=[])
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "products"
        exclude = ("transactions","plans", "plan" )


class Transaction(TimestampMixin, Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='transactions')
    product = fields.ForeignKeyField('models.Product', related_name='transactions')
    quantity = fields.IntField(null=True, default=1)
    amount = fields.IntField()
    channel = fields.CharField(max_length=255, null=True, default="Paystack")
    payment_ref = fields.IntField()
    trans_type = fields.IntEnumField(
        TransactionType, default=TransactionType.credit)
   
    class Meta:
        table = "transactions"




class Plan(TimestampMixin, Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='plans')
    product = fields.ForeignKeyField('models.Product', related_name='plan')
    amount_paid = fields.IntField(default=1)
    trans_ref = fields.ForeignKeyField('models.Transaction', related_name='transactions')
    blurbers_count = fields.IntField(null=True , default=10)
    file_upload_count = fields.IntField(default=0)
    # impressions_gotten
    imp_gotten = fields.IntField(null = False, default=1)
    start_date = fields.DatetimeField(null=True, auto_now_add=True)
    end_date = fields.DatetimeField(null=True, auto_now=True)
    dates = fields.JSONField(null = True, default=[])
    is_ended = fields.BooleanField(default=True)
    states = fields.JSONField(null = True, default=[])
    all_states = fields.BooleanField(null = True, default=True)

    class Meta:
        table = "plans"
        exclude = ("transactions", "user" )


Tortoise.init_models(['models'], 'models')
