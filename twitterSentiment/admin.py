from django.contrib import admin
from twitterSentiment.models import Company, TwitterText

admin.site.register(Company)
admin.site.register(TwitterText)
class CompanyAdmin(admin.ModelAdmin):
    fields = ['company_name']
