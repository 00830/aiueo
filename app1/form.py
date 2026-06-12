from django import forms

class RegisterUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix=""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password = forms.CharField(label="パスワード:", max_length=256)
    checkpassword = forms.CharField(label="パスワード(確認):", max_length=256)
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        checkpassword = cleaned.get("checkpassword")
        if password != checkpassword:
            raise forms.ValidationError("パスワードが一致しません。")
        return cleaned



    