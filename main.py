import serial.tools.list_ports
import time

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

def main():
    # Получаем список доступных портов
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        return

    # Выводим список доступных портов
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"{i + 1}. {port}")

    # Запрашиваем у пользователя выбор порта
    port_index = int(input("Enter port number to use (1 to {}): ".format(len(ports)))) - 1
    selected_port = ports[port_index]

    # Устанавливаем параметры порта
    baudrate = int(input("Enter baud rate (e.g., 9600): "))
    bytesize = 8  # Устанавливаем размер данных в 8 бит (1 байт)

    # Открываем выбранный порт
    ser = serial.Serial(selected_port)
    set_port_settings(ser, baudrate, bytesize)

    # Выводим информацию о порте
    print(f"Serial port '{selected_port}' opened with baud rate {baudrate} and data packet size {bytesize} bits.")

    try:
        while True:
            # Генерируем сообщение размером сколько то байт байта
            message = generate_message(32)

            # Отправляем сообщение
            ser.write(message)
            print(f"Sent message: {message.decode('utf-8')}")

            # Ждем 1 секунду перед отправкой следующего сообщения
            time.sleep(1)

    except KeyboardInterrupt:
        # При остановке программы (например, Ctrl+C) закрываем порт
        ser.close()
        print("\nSerial port closed.")

if __name__ == "__main__":
    main()
