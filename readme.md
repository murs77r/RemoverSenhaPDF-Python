# 🔓 Removedor de Senha de PDF (Flask App) 📄

Este repositório contém o código de uma aplicação web Flask que permite remover a senha de arquivos PDF protegidos. A aplicação oferece:

*   **Interface Web Simples:**  Formulário HTML com campos para upload de arquivo e inserção de senha.
*   **Descriptografia de PDF:** Utiliza a biblioteca `PyPDF2` para descriptografar o PDF fornecido.
*   **Download do Arquivo:** Permite baixar o PDF descriptografado com o nome `desprotegido.pdf`.
*   **Tratamento de Erros:**  Retorna mensagens de erro em caso de falha (arquivo não fornecido, senha incorreta, erro no processamento).
*   **Interface Amigável:** Design responsivo e limpo, utilizando a fonte Roboto. Botões para "Remover Senha" e "Limpar".

## ✨ Funcionalidades Principais

1.  **Upload de Arquivo:** O usuário seleciona um arquivo PDF protegido do seu computador.
2.  **Entrada de Senha:** O usuário digita a senha do PDF.
3.  **Processamento:** O backend (Flask/Python) recebe o arquivo e a senha, descriptografa o PDF (se a senha estiver correta) e prepara o arquivo para download.
4.  **Download:**  O usuário baixa o PDF descriptografado.
5. **Limpeza:** O usuário pode limpar os dados

## 🛠️ Tecnologias

*   **Python:** Linguagem de programação.
*   **Flask:** Microframework web para Python.
*   **PyPDF2:** Biblioteca Python para manipulação de PDFs.
*   **HTML, CSS, JavaScript:** Para a interface web (frontend).
*   **Google Fonts (Roboto):** Fonte utilizada.
* **`tempfile`**: Cria um arquivo temporário, para salvar o PDF para realizar a remoção de senhas.