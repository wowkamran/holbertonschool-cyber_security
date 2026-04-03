#!/usr/bin/python3
"""
Модуль для поиска и замены строки в куче (heap) запущенного процесса.
Этот скрипт обращается к /proc/[pid]/maps и /proc/[pid]/mem.
"""

import sys


def print_error(message):
    """Печатает сообщение об ошибке и выходит со статусом 1."""
    print(message)
    sys.exit(1)


def read_write_heap():
    """
    Находит кучу в картах памяти процесса и заменяет искомую строку.
    """
    # Проверка аргументов
    if len(sys.argv) != 4:
        print_error("Usage: read_write_heap.py pid search replace")

    pid = sys.argv[1]
    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    # Пути к файлам процесса в /proc
    maps_path = "/proc/{}/maps".format(pid)
    mem_path = "/proc/{}/mem".format(pid)

    # 1. Поиск границ кучи (heap) в файле maps
    heap_start = None
    heap_end = None

    try:
        with open(maps_path, 'r') as maps_file:
            for line in maps_file:
                if "[heap]" in line:
                    # Пример строки: 555e646e0000-555e64701000 rw-p ...
                    parts = line.split()
                    addr_range = parts[0].split('-')
                    heap_start = int(addr_range[0], 16)
                    heap_end = int(addr_range[1], 16)
                    break
    except Exception as e:
        print_error("Can't open or read maps: {}".format(e))

    if heap_start is None:
        print_error("Heap not found for process {}".format(pid))

    # 2. Поиск и замена строки в файле mem
    try:
        with open(mem_path, 'rb+') as mem_file:
            # Переходим к началу кучи
            mem_file.seek(heap_start)
            heap_data = mem_file.read(heap_end - heap_start)

            # Ищем строку (в байтах)
            search_bytes = search_str.encode('ascii')
            try:
                offset = heap_data.index(search_bytes)
            except ValueError:
                print_error("String '{}' not found in heap".format(search_str))

            # Переходим к точному адресу найденной строки
            mem_file.seek(heap_start + offset)
            # Записываем новую строку и добавляем нулевой байт (как в C)
            mem_file.write(replace_str.encode('ascii') + b'\0')

    except PermissionError:
        print_error("Run with sudo to access /proc/[pid]/mem")
    except Exception as e:
        print_error("Error: {}".format(e))


if __name__ == "__main__":
    read_write_heap()
