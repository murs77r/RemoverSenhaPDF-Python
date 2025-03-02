import os
import PyPDF2
from flask import Flask, request, jsonify, send_file, session
from io import BytesIO
import tempfile

app = Flask(__name__)
app.secret_key = os.urandom(24)

class DecryptionError(Exception):
    pass

class InvalidFileError(Exception):
    pass

def remover_senha_pdf(arquivo_pdf, senha):
    try:
        with open(arquivo_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            if not pdf_reader.is_encrypted:
                return {'info': "Este PDF não está protegido por senha."}

            if not pdf_reader.decrypt(senha):
                raise DecryptionError("Senha incorreta ou PDF não foi decriptado")

            pdf_writer = PyPDF2.PdfWriter()
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            with BytesIO() as output_pdf_stream:
                pdf_writer.write(output_pdf_stream)
                output_pdf_stream.seek(0)
                return {'success': True, 'data': output_pdf_stream}

    except PyPDF2.errors.PdfReadError:
        raise InvalidFileError("Arquivo PDF inválido ou corrompido.")
    except DecryptionError as e:
        raise DecryptionError(str(e))
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remover Senha de PDF</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            width: 100%;
            height: 100vh;
            max-width: none;
            max-height: none;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-sizing: border-box;
        }

        h1 {
            margin-bottom: 30px;
            color: #333;
            font-size: 2.5rem;
            font-weight: 700;
        }

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 700;
            color: #555;
        }

        input[type="file"],
        input[type="password"] {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1rem;
            font-family: 'Roboto', sans-serif;
        }

        input[type="file"] {
            cursor: pointer;
        }

        input[type="file"]::file-selector-button {
            font-family: 'Roboto', sans-serif;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-right: 10px;
        }

        input[type="file"]::file-selector-button:hover {
            background-color: #0056b3;
        }

        .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
            width: 100%;
            gap: 5px;
        }

        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.1s;
            font-family: 'Roboto', sans-serif;
            flex: 1;
        }

        button:hover {
            background-color: #218838;
            transform: translateY(-2px);
        }

        button.clear {
            background-color: #dc3545;
        }

        button.clear:hover {
            background-color: #c82333;
        }

        #results {
            margin-top: 30px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1rem;
            display: none;
            text-align: center;
        }

        .loading-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .loading-content {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }

        .loader {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 600px) {
          .container{
             border-radius: 0;
             box-shadow: none;
             padding: 20px;
         }
            h1 {
                font-size: 2rem;
            }

            input[type="file"],
            input[type="password"] {
                font-size: 0.9rem;
            }

            button {
                padding: 10px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Remover Senha de PDF</h1>
        <form id="pdf-form" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="pdfFile">Arquivo PDF:</label>
                <input type="file" id="pdfFile" name="pdfFile" accept=".pdf" required>
            </div>
            <div class="form-group">
                <label for="pdfPassword">Senha do PDF:</label>
                <input type="password" id="pdfPassword" name="pdfPassword" required>
            </div>
            <div class="button-container">
                <button type="button" onclick="submitForm()">Remover Senha</button>
                <button class="clear" type="button" onclick="clearFields()">Limpar</button>
            </div>
        </form>
        <div id="results"></div>
    </div>

    <div id="loading-modal" class="loading-modal">
        <div class="loading-content">
            <div class="loader"></div>
            <p>Processando...</p>
        </div>
    </div>

    <script>
    function clearFields() {
        if (confirm('Tem certeza que deseja limpar os campos?')) {
            document.getElementById('pdfFile').value = '';
            document.getElementById('pdfPassword').value = '';
            document.getElementById('results').innerHTML = '';
            document.getElementById('results').style.display = 'none';
        }
    }
    function toggleLoadingModal(show) {
        const modal = document.getElementById('loading-modal');
        modal.style.display = show ? 'flex' : 'none';
    }

    function submitForm() {
        const pdfFileInput = document.getElementById('pdfFile');
        if (pdfFileInput.files.length === 0) {
            alert('Por favor, selecione um arquivo PDF.');
            return;
        }

        if (!pdfFileInput.files[0].type.match('application/pdf')) {
            alert('O arquivo selecionado não é um PDF válido.');
            return;
        }

        const passwordInput = document.getElementById('pdfPassword');
        if (!passwordInput.value.trim()) {
            alert('Por favor, insira a senha do PDF.');
            return;
        }

        document.getElementById('results').style.display = 'none';
        toggleLoadingModal(true);

        const form = document.getElementById('pdf-form');
        const formData = new FormData(form);

        const submitButton = document.querySelector('button[type="button"]');
        submitButton.disabled = true;

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                if (response.headers.get('content-disposition')) {
                    return response.blob();
                } else {
                    return response.json();
                }
            } else {
                return response.json().then(data => {
                  throw new Error(data.error || 'Erro na resposta do servidor');
              });
            }
        })
        .then(data => {
            toggleLoadingModal(false);
            submitButton.disabled = false;

            if (data instanceof Blob) {
                const url = window.URL.createObjectURL(data);
                const a = document.createElement('a');
                a.href = url;
                a.download = document.getElementById('pdfFile').files[0].name.replace('.pdf', '_desprotegido.pdf');
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else if (data.info) {
                alert(data.info);
            }
        })
        .catch(error => {
            toggleLoadingModal(false);
            submitButton.disabled = false;
            alert(error.message);
        });
    }
 document.getElementById('pdf-form').addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm();
        });

    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session.clear()
        return HTML

    if request.method == 'POST':
        pdf_file = request.files.get('pdfFile')
        senha = request.form.get('pdfPassword')

        if not pdf_file or not senha.strip():
            return jsonify({'error': "Por favor, insira um arquivo PDF e uma senha!"}), 400

        if pdf_file.mimetype != 'application/pdf':
            return jsonify({'error': "O arquivo enviado não é um PDF válido."}), 400
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                pdf_file.save(temp_file.name)
                temp_file_path = temp_file.name

            nome_arquivo = os.path.basename(pdf_file.filename)
            nome_arquivo_sem_extensao, _ = os.path.splitext(nome_arquivo)

            result = remover_senha_pdf(temp_file_path, senha)

        except InvalidFileError as e:
            return jsonify({'error': str(e)}), 400
        except DecryptionError as e:
             return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            if 'temp_file_path' in locals():
                os.remove(temp_file_path)

        if 'success' in result:
             return send_file(
                result['data'],
                as_attachment=True,
                download_name=f"{nome_arquivo_sem_extensao}_desprotegido.pdf",
                mimetype='application/pdf'
            )
        else:
            return jsonify(result), 200
if __name__ == '__main__':
    app.run(debug=False)