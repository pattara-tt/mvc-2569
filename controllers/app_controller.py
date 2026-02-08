
class AppController:
    def __init__(self, root, views):
        self.root = root
        self.views = views
        self.session = {"email": None, "role": None}
        self.current = None

    # คุมการสลับหน้า
    def show(self, name: str, **kwargs):
        if self.current:
            self.current.hide()
        view = self.views[name]
        self.current = view
        view.show(**kwargs)

    # save session
    def login(self, email: str, role: str):
        self.session["email"] = email
        self.session["role"] = role

    # clear session
    def logout(self):
        self.session = {"email": None, "role": None}
        self.show("login")
