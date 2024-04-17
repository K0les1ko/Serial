import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import time

# Глобальная переменная для доступа к объекту Serial
serial_port = None

def list_serial_ports():
    """ Возвращает список доступных последовательных портов """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def set_port_settings(port, baudrate, bytesize):
    """ Устанавливает параметры порта: скорость и размер пакета данных """
    port.baudrate = baudrate
    port.bytesize = bytesize

def generate_message(size):
    """ Генерирует строку 'test' повторенную до указанного размера (в байтах) """
    message = "test" * (size // 4)  # Повторяем строку 'test' нужное количество раз
    return message.encode('utf-8')  # Преобразуем строку в байты

def send_message(ser, message):
    """ Отправляет сообщение через COM-порт """
    ser.write(message)
    print(f"Sent message: {message.decode('utf-8')}")

def start_sending(ser, message_size, send_interval):
    """ Начинает циклическую отправку сообщений через COM-порт """
    try:
        while True:
            # Генерируем сообщение
            message = generate_message(message_size)

            # Отправляем сообщение
            send_message(ser, message)

            # Ждем указанный интервал перед отправкой следующего сообщения
            time.sleep(send_interval)

    except KeyboardInterrupt:
        # При остановке программы (например, Ctrl+C) закрываем порт
        ser.close()
        print("\nSerial port closed.")

def stop_sending():
    """ Останавливает отправку сообщений """
    global serial_port
    if serial_port:
        serial_port.close()
        print("\nSerial port closed.")

def start_serial_communication(selected_port, baudrate, message_size, send_interval):
    """ Начинает взаимодействие с выбранным COM-портом """
    global serial_port
    ser = serial.Serial(selected_port)
    set_port_settings(ser, baudrate, 8)  # Размер данных всегда 8 бит (1 байт)
    print(f"Serial port '{selected_port}' opened with baud rate {baudrate} and data packet size 8 bits.")
    serial_port = ser  # Сохраняем объект Serial для возможности остановки
    start_sending(ser, message_size, send_interval)

def main():
    # Создаем графический интерфейс
    root = tk.Tk()
    root.title("Serial Communication")

    # Получаем список доступных портов
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        return

    # Создаем выпадающий список для выбора порта
    port_label = ttk.Label(root, text="Select a port:")
    port_label.pack()
    port_var = tk.StringVar(root)
    port_dropdown = ttk.Combobox(root, textvariable=port_var, values=ports)
    port_dropdown.pack()

    # Поля для ввода параметров порта
    baudrate_label = ttk.Label(root, text="Enter baud rate:")
    baudrate_label.pack()
    baudrate_entry = ttk.Entry(root)
    baudrate_entry.pack()

    # Поля для ввода параметров сообщения
    message_size_label = ttk.Label(root, text="Enter message size (bytes):")
    message_size_label.pack()
    message_size_entry = ttk.Entry(root)
    message_size_entry.pack()

    # Поля для ввода интервала отправки сообщений
    send_interval_label = ttk.Label(root, text="Enter send interval (seconds):")
    send_interval_label.pack()
    send_interval_entry = ttk.Entry(root)
    send_interval_entry.pack()

    # Кнопка для запуска взаимодействия
    start_button = ttk.Button(root, text="Start", command=lambda: start_serial_communication(
        port_dropdown.get(),
        int(baudrate_entry.get()),
        int(message_size_entry.get()),
        float(send_interval_entry.get())
    ))
    start_button.pack()

    # Кнопка для остановки отправки сообщений
    stop_button = ttk.Button(root, text="Stop", command=stop_sending)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
