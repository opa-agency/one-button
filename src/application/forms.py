from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class PartnerSignUpForm(UserCreationForm):
    """User creation form that uses email as the login identifier."""

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    full_name = forms.CharField(
        label="Nume",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "full_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the username field – we drive it from the email address.
        self.fields["username"].required = False
        self.fields["username"].widget = forms.HiddenInput()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        UserModel = get_user_model()
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Exista deja un cont cu acest email.")
        return email

    def clean_full_name(self):
        name = self.cleaned_data["full_name"].strip()
        if not name:
            raise forms.ValidationError("Te rugam sa completezi numele tau.")
        return name

    def save(self, commit=True):
        email = self.cleaned_data["email"].lower()
        name = self.cleaned_data["full_name"].strip()
        user = super().save(commit=False)
        user.username = email
        user.email = email
        if " " in name:
            parts = [part for part in name.split(" ") if part]
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:])
        else:
            user.first_name = name
            user.last_name = ""
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """Authentication form that accepts an email address instead of username."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            UserModel = get_user_model()
            try:
                user_obj = UserModel.objects.get(email__iexact=email)
                self.cleaned_data["username"] = user_obj.get_username()
            except UserModel.DoesNotExist:
                # Fall back to the raw email; authentication will fail cleanly.
                self.cleaned_data["username"] = email
        return super().clean()
