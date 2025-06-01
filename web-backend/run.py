from app import create_app

app = create_app()

# if __name__ == '__main__':
#     app.run(port=5111, debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=0)  # Flask自动选择一个可用端口