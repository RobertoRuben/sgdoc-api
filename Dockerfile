# Usar imagen base de Windows con Python
FROM mcr.microsoft.com/windows/servercore:1809 as builder

# Descargar e instalar Python 3.11
SHELL ["powershell", "-Command"]
RUN Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -OutFile python-3.11.0-amd64.exe ; \
    Start-Process python-3.11.0-amd64.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait ; \
    Remove-Item python-3.11.0-amd64.exe

# Configurar zona horaria
ENV TZ=America/Lima

WORKDIR C:/app

# Copiar archivos de requerimientos
COPY requirements.txt .
COPY .env .

# Instalar dependencias
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src

EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]