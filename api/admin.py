from django.contrib import admin
from api.models import (
    LoanType,
    Loan,
    Payment
)


# Register your models here.
admin.site.register([LoanType,Loan,Payment])