
# Atarefado 📚

Aplicativo desktop de gerenciamento de tarefas desenvolvido em Python.

## Funcionalidades

- Adicionar tarefas.
- Marcar tarefas como concluídas ou pendentes.
- Excluir tarefas.
- Limpar tarefas concluídas.
- Contabilizar tarefas concluídas e pendentes.
- Salvar tarefas localmente.
- Interface gráfica com ícone personalizado.

## Tecnologias

- Python
- Tkinter
- JSON
- PyInstaller

## Como executar

1. Instale o Python.
2. Baixe este repositório.
3. Abra a pasta do projeto no terminal.
4. Execute:

   python main.py

## Como gerar o executável

Instale o PyInstaller:

python -m pip install pyinstaller

Gere o executável no Windows:

python -m PyInstaller --clean --onefile --windowed --name Atarefado --icon=Atarefado.ico main.py

O executável será criado na pasta dist.

## Autor

Samuel Betini de Amorim

Projeto pessoal desenvolvido para praticar programação e criação de aplicações desktop.