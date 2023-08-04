import psutil
import csv
import time

def monitorizar_recursos():
    with open('uso_recursos.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Tempo (s)', 'Uso do CPU (%)', 'Uso de RAM (%)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        segundos = 0
        while True:
            uso_cpu = psutil.cpu_percent(interval=0.2)
            uso_ram = psutil.virtual_memory().percent
            print(f'Tempo: {segundos:.1f}s | Uso do CPU: {uso_cpu:.2f}% | Uso de RAM: {uso_ram:.2f}%')

            writer.writerow({'Tempo (s)': segundos, 'Uso do CPU (%)': uso_cpu, 'Uso de RAM (%)': uso_ram})

            segundos += 0.2

if __name__ == "__main__":
    try:
        monitorizar_recursos()
    except KeyboardInterrupt:
        print("\nMonitorização terminada. Os dados foram salvos no arquivo uso_recursos.csv.")

