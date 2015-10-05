"""
Custom sort utility:
    - validate input SORT attribute value against whitelist SORT_DICT
    - reverse sorting direction for template
"""

#Dictionary of allowed sorting values for SqlAlchemy order_by
SORT_DICT = {'-department':'upper(hr_departments.department_name) desc',
             '+department':'upper(hr_departments.department_name) asc',
             '+employee':'upper(hr_employees.first_name || hr_employees.last_name) asc',
             '-employee':'upper(hr_employees.first_name || hr_employees.last_name) desc',
             '+salary':'hr_employees.salary asc',
             '-salary':'hr_employees.salary desc',
             '+hired':'hr_employees.hire_date asc',
             '-hired':'hr_employees.hire_date desc',
             '+hireend':'hr_employees.end_date asc',
             '-hireend':'hr_employees.end_date desc',
             '+application':'upper(t_object.name) asc',
             '-application':'upper(t_object.name) desc',
             '+alias':'upper(t_object.alias) asc',
             '-alias':'upper(t_object.alias) desc',
             '+stereotype':'upper(t_object.stereotype) asc',
             '-stereotype':'upper(t_object.stereotype) desc',
             '+lifecycle':'upper(t_object.status) asc',
             '-lifecycle':'upper(t_object.status) desc',
             '+lang':'upper(t_object.gentype) asc',
             '-lang':'upper(t_object.gentype) desc',}

class SortValue:
    """Sort input validation and Sql Order By string mapping"""

    def __init__(self, sort_parameter):
        self.sort_parameter = sort_parameter

    def _validate(self):
        """URL Query sort attribute validation"""
        if self.sort_parameter in SORT_DICT:
            return True
        return False

    def sort_str(self):
        """Return order_by string validated by key"""
        if self._validate():
            return SORT_DICT[self.sort_parameter]
        return ''

    def reverse_direction(self):
        """Reverses sort direction for two-way sorting"""
        direction = ''
        if self.sort_parameter[0] == '+':
            direction = self.sort_parameter.replace('+', '-', 1)
        if self.sort_parameter[0] == '-':
            direction = self.sort_parameter.replace('-', '+', 1)
        return direction[0]
