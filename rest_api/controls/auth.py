from flask import render_template

def is_admin(current_user):
    if hasattr(current_user,"role") and current_user.role=="admin":
        return True
    
    else:
        return False

def is_user(current_user):
    if hasattr(current_user, "role"):
        return False
    else:
        return True
def is_staff(current_user):
    if not hasattr(current_user, "role"):
        return False
    if current_user.role != "staff":
        return False
    return True

def is_company_admin(current_user):
    if not hasattr(current_user, "role"):
        return False
    if current_user.role != "company_admin":
        return False
    return True

def is_admin_or_company_admin_of_the_same_company(current_user, company_id):
    # if it's customer
    if not hasattr(current_user, "role"):
        return False

    if current_user.role=="admin":
        return True

    if current_user.role=="company_admin" and current_user.company_id==company_id:
        return True

    return False


def render_error_page_unauthorized_access():
    return render_template("error.html", message = "unauthorized access")


def render_error_page_wrong_password():
    return render_template("error.html", message="wrong password")