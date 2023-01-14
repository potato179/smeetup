# from controller import home

def routes_list(app):
    from controller import UserController, BoardController
    app.add_namespace(UserController.User)
    app.add_namespace(BoardController.board)
    return app
