"""
Application general form logic.
Secure BaseForm for extention in every app_*
"""
from wtforms.ext.csrf.session import SessionSecureForm
from wtforms.validators import ValidationError



#For CSRF security override with Pyramid session get_csrf_token
class BaseForm(SessionSecureForm):
    """Other forms must extend this secure form class"""
    def generate_csrf_token(self, session):
        """Get the session's CSRF token."""
        return session.get_csrf_token()

    def validate_csrf_token(form, field):
        """Validate the CSRF token."""
        if field.data != field.current_token:
            raise ValidationError('Invalid CSRF token; the form probably expired.  Try again.')


