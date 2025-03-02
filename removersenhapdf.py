from flask import Flask, request, jsonify, send_file
from PyPDF2 import PdfReader, PdfWriter
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def remove_pdf_password():
    if request.method == 'GET':
        return open("index.html").read()

    if 'pdfFile' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    pdf_file = request.files['pdfFile']
    password = request.form.get('pdfPassword')

    if not password:
        return jsonify({"error": "Senha não fornecida."}), 400

    try:
        reader = PdfReader(pdf_file)
        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "output.pdf")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return send_file(output_path, as_attachment=True, download_name="desprotegido.pdf")

    except Exception as e:
        return jsonify({"error": f"Erro ao processar o PDF: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)