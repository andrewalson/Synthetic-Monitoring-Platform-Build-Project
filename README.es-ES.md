

# <p align="center"> Proyecto de Desarrollo de una Plataforma de Monitoreo Sintético </p>

<p align="center"> Con una tasa de crecimiento anual compuesta proyectada del 15.3% de 2023 a 2028, el monitoreo sintético es una industria global de rápido crecimiento. Esa cifra refleja una época en la que incidentes como la interrupción mundial de sistemas Windows en julio de 2024, causada por una actualización defectuosa y lanzada imprudentemente de la configuración del sensor de CrowdStrike, pueden generar miles de millones en daños no asegurados. Por lo tanto, en el mundo actual, el monitoreo activo es una disciplina de alto impacto y de una importancia difícil de subestimar. Durante este "Proyecto de Desarrollo" de 8 semanas, asociado con la Beca de Desarrollo Open Avenues y dirigido por el Becario de Desarrollo Sonu Gupta, desarrollé una plataforma de monitoreo sintético que puede monitorear el rendimiento de una aplicación o sistema enviando pings a servidores para obtener datos de series temporales desde la línea de comandos o la interfaz de usuario de Flask, y retransmitiéndolos a través de Prometheus hacia un panel de Grafana para su visualización.</p>

<p align="center">
<img alt="Captura de pantalla 2024-08-23 a las 7 32 12 PM" src="https://github.com/user-attachments/assets/68be96cb-f5c3-4023-a848-9ad0f8b2e683">
</p>

## <p align="center"> Componentes del Sistema: </p>

### Analizador de Archivos de Configuración YAML

- Módulo de Python que lee y analiza archivos de configuración YAML para devolverlos como un diccionario de Python.
- Detecta claves de nivel superior y tipos de configuración comunes basándose en la estructura YAML cuando se ejecuta de forma independiente.
- Maneja varios escenarios de errores como archivo no encontrado, sintaxis YAML inválida, etc.

### Monitor de Conectividad de Red

- Módulo de Python que aprovecha la biblioteca **'pingparsing'** para monitorear la conectividad de red.
- Toma los objetivos, sondas e intervalo desde la entrada del usuario, envía pings al(s) servidor(es) después del intervalo dado y analiza los resultados.
- Inicializa las métricas de Prometheus para cada servidor objetivo y cada métrica de latencia/pérdida de paquetes a exponer.
  - **Métricas Expuestas a Prometheus:**
  - Conteo de Paquetes Transmitidos/Recibidos/Pérdidas/Duplicados
  - Tiempo de Ida y Vuelta (RTT) Promedio/Mejor/Peor
  - Desviación Media del Tiempo de Ida y Vuelta (Jitter)
  - Tasa de Pérdida de Paquetes
  - Tasa de Duplicación de Paquetes
- Extrae y presenta las métricas clave en la consola con confirmación de la actualización de las métricas de Prometheus.
  - **Métricas Mostradas en CLI/GUI:** RTT Promedio/Mejor/Peor, Tasa de Pérdida/Duplicación de Paquetes, Jitter

### Módulos Integrados @ main.py

- Script principal de Python que integra los módulos del analizador de archivos YAML y el monitor de conectividad de red.
- Inicia el servidor HTTP (en prometheus.yml) en el puerto 8989.
- Toma un argumento de línea de comandos para la ruta del archivo YAML (de lo contrario, se utiliza uno predeterminado).
- Lee el archivo YAML y obtiene una lista de servidores, enviando pings a cada servidor objetivo después del intervalo especificado.
- Muestra las métricas de ping en la consola mientras establece las métricas de Prometheus con `ping_monitor.display_and_expose_results()`.

### Punto de Entrada de la Interfaz Frontend de Flask y Flujo de Salida

- Módulo de Python que integra el microframework Flask para crear una interfaz frontend para la plataforma de monitoreo.
- Acepta la ruta del archivo YAML e inicia el programa, redirigiendo la salida a un registro persistente accesible desde la página principal.
- Borra los mensajes anteriores y ejecuta con una nueva configuración con un solo clic.

### Prometheus & Grafana

- Prometheus: Sistema de monitoreo y herramienta de alertas de código abierto configurado para extraer métricas del monitor de ping.
- Grafana: Plataforma de observabilidad y herramienta de visualización de código abierto con paneles de datos de series temporales configurados.

## <p align="center"> Paneles de Ejemplo del Dashboard: </p>

<p align="center">
<img alt="Dashboard de Ejemplo" src="https://github.com/user-attachments/assets/e7034551-6391-4449-bf35-7c5721fb58f5">
</p>

## <p align="center"> Interfaz de Usuario de Flask: </p>

<p align="center">
<img alt="Flujo de Salida" src="https://github.com/user-attachments/assets/d3a63179-5269-46e8-ac37-db32de56c781">
</p>

## <p align="center"> Cómo Empezar </p>

_Prerrequisitos: Binarios de Prometheus y Grafana, Python 3.8+_

- Clona el repositorio.
- **[Opcional]** Agrega tu archivo de configuración YAML al directorio `configs/`.
- Agrega el puerto del servidor HTTP a la configuración de Prometheus.
- Navega al directorio de Prometheus y ejecuta Prometheus: `./prometheus --config.file=prometheus.yml`
- Navega al directorio de Grafana y ejecuta Grafana: `./bin/grafana-server`
- Abre e inicia sesión en Grafana en [http://localhost:3000](http://localhost:3000) con un navegador.
- Agrega Prometheus [http://localhost:9090](http://localhost:9090) como una [fuente de datos](https://grafana.com/docs/grafana/latest/datasources/) en Grafana.
- Navega al directorio raíz del repositorio clonado.
- Instala las dependencias del proyecto:

```zsh
  pip install -r requirements.txt
```

- **CLI:** Ejecuta el script principal en `main.py` y pasa la ruta del archivo YAML con los servidores objetivo (se proporciona uno predeterminado si no hay argumento de configuración):
  - **Nota:** En ciertos entornos utiliza `python3`

```zsh
  python src/main.py configs/example.yml
```

- **Interfaz Flask:** Ejecuta `frontend.py` en el directorio `flask_frontend` y navega al servidor de desarrollo en [http://127.0.0.1:5000](http://127.0.0.1:5000) en un navegador.

```zsh
  flask --app src/flask_frontend/frontend.py run
```

- **Si proporcionas un archivo YAML personalizado (que no sea el predeterminado variety.yaml), formatea como:**

```
global_settings:
  probes: 4
  interval: 1
  port: 8989

targets:
  - 8.8.8.8
  - example.com
  - another.target.io
```
