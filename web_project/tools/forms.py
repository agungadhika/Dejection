from django import forms

class FormField(forms.Form):
    url_field = forms.URLField(label="Input URL", label_suffix=None)
    vuln = (
        ('xss', 'Cros-site Scripting'),
        ('sqli', 'SQL Injection'),
        ('command', 'Command Injection'),
        ('xxe', 'XXE Injection'),
        ('nosql', 'NoSQL Injection'),
    )
    type_attack = forms.ChoiceField(choices = vuln)

    CHOICES = [
        ("GET", "GET Method"),
        ("POST", "POST Method")
    ]
    attack_method = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(FormField, self).__init__(*args, **kwargs)
        self.fields['url_field'].label = 'Input URL'  # Atur ulang label field
        # self.fields['url_field'].widget.attrs.update({'style': 'font-size: 12px'})
        # self.fields['url_field'].label_suffix = None  # Hilangkan tanda titik dua (:)
        self.fields['url_field'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['url_field'].widget.attrs.update({'placeholder': 'Masukkan URL'})
        self.fields['type_attack'].widget.attrs.update({'class': 'form-control'})
        # self.fields['attack_method'].widget.attrs.update({'class': 'form-check',})
    # integer_field = forms.IntegerField()