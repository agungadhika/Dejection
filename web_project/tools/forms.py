from django import forms

class FormField(forms.Form):
    url_field = forms.URLField(label="Input Url")
    vuln = (
        ('xss', 'Cros-site Scripting'),
        ('sqli', 'SQL Injection'),
        ('command', 'Command Injection'),
        ('xxe', 'XXE Injection'),
        ('nosql', 'NoSQL Injection'),
    )
    type_attack = forms.ChoiceField(choices = vuln)
    

    # integer_field = forms.IntegerField()
