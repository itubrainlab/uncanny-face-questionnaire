from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8000)


## TODO
# 4. Stop people from accessing retired user_ids