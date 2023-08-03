import psutil
import csv
import time

def monitorizar_cpu():
    with open('uso_cpu.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Tempo (s)', 'Uso do CPU (%)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        segundos = 0
        while True:
            uso_cpu = psutil.cpu_percent(interval=1)
            print(f'Tempo: {segundos}s | Uso do CPU: {uso_cpu:.2f}%')

            writer.writerow({'Tempo (s)': segundos, 'Uso do CPU (%)': uso_cpu})

            segundos += 1

if __name__ == "__main__":
    try:
        monitorizar_cpu()
    except KeyboardInterrupt:
        print("\nMonitorização do CPU terminado.")

