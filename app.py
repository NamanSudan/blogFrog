from website import create_app

# this is the main function that makes sure that the app file runs
if __name__ == "__main__":
    # this is the app
    app = create_app()
    # this is the main function
    app.run(debug=True)