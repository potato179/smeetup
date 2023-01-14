# from controller import home

def routes_list(app):
    from controller import UserController
    app.add_namespace(UserController.user)
    return app
