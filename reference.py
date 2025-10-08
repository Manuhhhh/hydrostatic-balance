import os
import glob
import pandas as pd
import serial
import time

# Configuración
carpeta_csv = "C:/Users/Usuario/OneDrive/Desktop/arduino_csv"
arduino_port = "COM5"
baud_rate = 9600
delta = 0.05
tiempo_estable_seg = 2
frecuencia_muestreo = 10

def encontrar_csv(carpeta):
    archivos = glob.glob(os.path.join(carpeta, "*.csv"))
    if archivos:
        return archivos[0]  # toma el primer CSV encontrado
    return None

def detectar_peso_estable(datos, delta, tiempo_estable_seg, freq):
    cantidad_minima = tiempo_estable_seg * freq
    inicio = 0
    secuencia_estable = []
    for i in range(1, len(datos)):
        if abs(datos[i] - datos[i-1]) <= delta:
            secuencia_estable.append(datos[i])
            if len(secuencia_estable) >= cantidad_minima:
                return sum(secuencia_estable)/len(secuencia_estable)
        else:
            secuencia_estable = [datos[i]]  # reinicia la secuencia
    return None  # si no se encuentra secuencia estable

def main():
    archivo = encontrar_csv(carpeta_csv)
    if not archivo:
        print("No se encontró ningún archivo CSV en la carpeta.")
        return

    print(f"Usando archivo CSV: {archivo}")
    df = pd.read_csv(archivo)
    
    # Ajusta el nombre de la columna si es necesario
    columna_peso = df.columns[0]
    datos = df[columna_peso].tolist()

    # Detecta peso en el aire
    peso_aire = detectar_peso_estable(datos, delta, tiempo_estable_seg, frecuencia_muestreo)
    if peso_aire is None:
        print("No se encontró un peso estable en el aire.")
        return

    # Detecta peso sumergido: asumimos que viene después del peso en aire
    indice_inicio = datos.index(min(datos, key=lambda x: abs(x - peso_aire))) + int(frecuencia_muestreo * tiempo_estable_seg)
    datos_sumergido = datos[indice_inicio:]
    peso_sumergido = detectar_peso_estable(datos_sumergido, delta, tiempo_estable_seg, frecuencia_muestreo)
    if peso_sumergido is None:
        print("No se encontró un peso estable sumergido.")
        return

    print(f"Peso en el aire: {peso_aire:.2f} N")
    print(f"Peso sumergido: {peso_sumergido:.2f} N")

    # Enviar a Arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=2)
        time.sleep(2)  # espera que Arduino reinicie
        arduino.write(f"{peso_aire:.2f},{peso_sumergido:.2f}\n".encode())
        print("Datos enviados a Arduino ✅")
        arduino.close()
    except Exception as e:
        print(f"No se pudo conectar a Arduino: {e}")

if __name__ == "__main__":
    main()
