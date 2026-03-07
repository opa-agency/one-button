from django import forms


class DashboardIdentityForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Numele tau (optional)",
                "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:border-slate-400 focus:outline-none",
            }
        ),
    )
    message = forms.CharField(
        max_length=280,
        required=False,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Mesajul tau (optional)",
                "rows": 3,
                "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:border-slate-400 focus:outline-none",
            }
        ),
    )
