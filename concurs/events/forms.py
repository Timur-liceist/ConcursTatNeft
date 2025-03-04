from django import forms


class SearchForm(forms.Form):
    request_content = forms.CharField(
        max_length=1023,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "style": "background-color:rgb(69, 69, 69); color: white;",
                "placeholder": "Search...",
            },
        ),
    )
