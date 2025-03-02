# 🔓 Removedor de Senha de PDF (Flask App) 📄

Este repositório contém o código de uma aplicação web Flask simples que permite remover a senha de arquivos PDF. A aplicação fornece uma interface HTML básica para upload de arquivos, inserção de senha e download do PDF descriptografado.

## ✨ Funcionalidades

*   **Upload de Arquivo PDF:**  O usuário pode selecionar um arquivo PDF protegido por senha do seu computador.
*   **Inserção de Senha:**  O usuário fornece a senha do PDF em um campo de texto.
*   **Remoção da Senha:**  O script Python (usando a biblioteca `PyPDF2`) descriptografa o PDF, removendo a proteção por senha.
*   **Download do PDF Desprotegido:**  Se a senha estiver correta, o usuário pode baixar o arquivo PDF sem senha. O nome do arquivo baixado será o nome original, com o sufixo `_desprotegido`.
*   **Tratamento de Erros:**
    *   Exibe mensagens de erro claras se o arquivo não for fornecido, a senha estiver incorreta ou o arquivo for inválido/corrompido.
    *   Lida com erros inesperados.
    *   Informa ao usuário se o PDF não estiver protegido por senha.
*   **Interface Web Amigável:**
    *   Design responsivo (se adapta a diferentes tamanhos de tela).
    *   Uso de HTML, CSS e JavaScript.
    *   Estilo básico com a fonte Roboto (Google Fonts).
    *   Botões para "Remover Senha" e "Limpar" campos.
    *   Modal de "carregamento" (loading) durante o processamento.
*   **Segurança (básica):**
    *   Uso de `app.secret_key` (embora a segurança real em um ambiente de produção exija práticas mais robustas).
    *   Utilização de arquivos temporários que são excluídos após o processamento.
*   **Limpeza de Sessão:** Limpa os dados da sessão (`session.clear()`) quando o usuário acessa a página principal (método GET).

## 🛠️ Tecnologias Utilizadas

*   **Python:** Linguagem de programação principal.
*   **Flask:** Framework web para Python (para criar a interface web e lidar com requisições).
*   **PyPDF2:** Biblioteca Python para manipulação de arquivos PDF (leitura, escrita, descriptografia).
*   **HTML, CSS, JavaScript:** Para a interface web (frontend).
* **`io` (BytesIO):** Para manipular o PDF em memória, sem precisar criar arquivos intermediários no sistema de arquivos.
* **`tempfile`**: Cria um arquivo temporário, para salvar o PDF para realizar a remoção de senhas.
*   **Google Fonts (Roboto):**  Fonte usada na interface.

## 📁 Estrutura do Código (Simplificada)

*   **`remover_senha_pdf(arquivo_pdf, senha)`:**  Função principal que recebe o caminho do arquivo PDF e a senha, e tenta remover a senha.  Retorna um dicionário com o resultado (sucesso ou informação) ou levanta exceções em caso de erro.
*   **`HTML`:**  Variável que contém o código HTML da interface web (formulário, botões, etc.).
*   **`@app.route('/', methods=['GET', 'POST'])`:**  Define a rota principal da aplicação (`/`).
    *   `GET`:  Exibe a interface HTML (e limpa a sessão).
    *   `POST`:  Recebe o arquivo PDF e a senha, chama a função `remover_senha_pdf`, e retorna o PDF desprotegido (se a senha estiver correta) ou uma mensagem de erro.
*   **`if __name__ == '__main__':`:**  Inicia o servidor de desenvolvimento do Flask (com `debug=True`, o que *não* é recomendado para produção).
*   **JavaScript (dentro do HTML):** Funções para lidar com a interação do usuário:
    *    `submitForm()`: Trata o envio do formulário, faz a requisição para o backend, exibe o modal de carregamento e manipula a resposta (download do PDF ou exibição de mensagens).
    *   `clearFields()`: Limpa os campos do formulário.
    *   `toggleLoadingModal()`: Controla a exibição do modal de carregamento.