# from controller import home

def routes_list(app):
    from controller import UserController, HomeController
    app.add_namespace(UserController.user)
    app.add_namespace(HomeController.home)
    return app
