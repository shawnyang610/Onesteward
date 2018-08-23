
import sys
import os
from werkzeug.security import generate_password_hash 

print('Creating all database tables')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))


# Create the database tables, add some initial data, and commit to the database
from rest_api import db # noqa
from rest_api.models.address import AddressModel # noqa
from rest_api.models.attachment import AttachmentModel # noqa
from rest_api.models.company import CompanyModel # noqa
from rest_api.models.jwt import RevokedTokenModel # noqa
from rest_api.models.order import OrderModel # noqa
from rest_api.models.staff import StaffModel # noqa
from rest_api.models.tracking import TrackingModel # noqa
from rest_api.models.user import UserModel # noqa


# Drop all of the existing database tables
db.drop_all()

# Create the database and the database table
db.create_all()

def add_super_company_user():

    first_company = CompanyModel.find_by_name("OneSteward")

    if not first_company:
        first_company = CompanyModel(
            "OneSteward",
            "admin@onesteward.com",
            "555-555-5555")
        first_company.save_to_db()

    first_staff = StaffModel.find_by_name("admin")
    if not first_staff:
        first_staff = StaffModel(
            "admin",
            "admin",
            generate_password_hash("admin_password"),
            first_company.id)

        first_staff.save_to_db()

    first_user = UserModel.find_by_name("NA")
    if not first_user:
        first_user = UserModel(
            generate_password_hash("admin_password"),
            name = "NA",
            email="NA",
            phone="")

        first_user.save_to_db()

add_super_company_user()

print('...done!')
