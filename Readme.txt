# PlayerPython

Este é um simples reprodutor de áudio em Python que suporta múltiplos formatos de áudio, como MP3, WAV, e FLAC. O projeto utiliza as bibliotecas `pygame`, `mutagen`, `pydub` e `tkinter` para fornecer uma interface gráfica para reprodução de músicas.

## Requisitos

### Windows

Para rodar o PlayerPython no Windows, é necessário instalar o `FFmpeg`, que é utilizado para lidar com alguns formatos de áudio como o FLAC.

#### Passos para instalar o FFmpeg no Windows:

1. Baixe o arquivo compactado do [FFmpeg](https://ffmpeg.org/download.html).
2. Extraia o arquivo compactado (`FFMPEG.7z`).
3. Mova a pasta extraída para o diretório `C:\Program Files (x86)\`.
4. Copie o caminho da pasta `bin` dentro do diretório extraído.
   - Exemplo: `C:\Program Files (x86)\ffmpeg\bin`
5. Abra o menu de **Variáveis de Ambiente** do Windows:
   - No Windows 10/11: clique com o botão direito em "Este PC" > "Propriedades" > "Configurações Avançadas do Sistema" > "Variáveis de Ambiente".
6. Na seção **Variáveis de Sistema**, localize e edite a variável `Path`.
7. Adicione o caminho do diretório `bin` do FFmpeg copiado no passo 4.
   - Exemplo: `C:\Program Files (x86)\ffmpeg\bin`.
8. Clique em "OK" para salvar as alterações.

Após seguir esses passos, o FFmpeg estará disponível globalmente em seu sistema.

### Linux

Se você está utilizando Linux, instale o FFmpeg usando o terminal com os seguintes comandos:

```bash
sudo apt update
sudo apt install ffmpeg
sudo apt upgrade
