---

# Scanner de Portas Simples

Este é um **scanner de portas simples** desenvolvido em Python. 
Ele permite que você realize uma varredura em um intervalo de portas em um endereço IP especificado, e exibe quais portas estão abertas.

![Tela](https://github.com/user-attachments/assets/35770362-84ce-47e5-a340-f4afebca1ecf)


https://github.com/user-attachments/assets/cfe46c21-205a-4c43-a8e9-02c6613f1b68

## Requisitos

Antes de rodar a aplicação, certifique-se de que os seguintes requisitos estejam atendidos:

### Python

A aplicação foi desenvolvida utilizando Python 3. 
Caso você não tenha o Python 3 instalado, siga as instruções abaixo para instalá-lo no seu sistema operacional.

#### **No Linux (Ubuntu/Debian/Kali)**

1. Abra o terminal e atualize a lista de pacotes:
   ```bash
   sudo apt update
   ```

2. Instale o Python 3:
   ```bash
   sudo apt install python3
   ```

3. Verifique se o Python foi instalado corretamente:
   ```bash
   python3 --version
   ```

### Dependências

A aplicação requer o módulo `tk` para a interface gráfica. Você pode instalar as dependências executando os seguintes comandos.

#### **No Linux (Ubuntu/Debian/Kali)**

1. Instale as dependências necessárias:
   ```bash
   sudo apt install python3-tk
   ```

2. Instale o `tk` com o `pip`:
   ```bash
   pip install tk
   ```

## Instalação

1. Clone ou baixe o repositório para o seu computador:
   ```bash
   git clone https://github.com/alanleandro23/Scanner_portas
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd scanner_portas.py
   ```

3. Se necessário, crie um ambiente virtual para instalar as dependências (recomendado):

   No **Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

Após a instalação das dependências, execute o script para rodar o scanner de portas:

1. No **Linux**:
   ```bash
   python3 scanner_portas.py
   ```

A aplicação será iniciada, e você poderá realizar a varredura de portas especificando o endereço IP e o intervalo de portas.

## Estrutura do Projeto

- `scanner_portas.py` - Arquivo principal do scanner de portas.
- `requirements.txt` - Lista das dependências necessárias para o projeto.

## Contribuições

Contribuições são bem-vindas! Se você deseja contribuir, por favor, faça um **fork** do repositório, crie uma branch para sua feature ou correção, e envie um **pull request**.

--- 
