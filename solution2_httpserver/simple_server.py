from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Загружаем HTML-файл контактов из общей папки templates
        try:
            with open('../templates/contacts.html', 'r', encoding='utf-8') as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, "Файл не найден")
        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")

    def do_POST(self):
        # Обрабатываем POST-запрос
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Парсим данные формы
        fields = parse_qs(post_data)

        # Извлекаем данные
        name = fields.get('name', [''])[0]
        email = fields.get('email', [''])[0]
        message = fields.get('message', [''])[0]

        # Печатаем в консоль
        print("=" * 50)
        print("POST данные получены:")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")
        print("=" * 50)

        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        response_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Данные получены</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success" role="alert">
                    <h4 class="alert-heading">Спасибо!</h4>
                    <p>Ваши данные успешно получены и обработаны.</p>
                    <hr>
                    <p class="mb-0"><a href="/" class="btn btn-primary">Вернуться на главную</a></p>
                </div>
            </div>
        </body>
        </html>
        """

        self.wfile.write(response_html.encode('utf-8'))


def run_server():
    host = 'localhost'
    port = 8080  # Используем другой порт, чтобы не конфликтовал с Flask

    server = HTTPServer((host, port), SimpleHandler)
    print(f"Сервер задания 2 запущен на http://{host}:{port}")
    print("На любой GET-запрос возвращается страница 'Контакты'")
    print("POST-запросы выводятся в консоль")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.shutdown()


if __name__ == '__main__':
    run_server()