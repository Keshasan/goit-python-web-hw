import shutil
from pathlib import Path
import os
from sys import argv, platform
import re


class Sorter:
    
    def normalize(self, name):
        table_symbols = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ', (
            'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r',
            's',
            't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', 'A', 'B', 'V', 'H', 'G', 'D', 'E',
            'Ye',
            'Zh', 'Z', 'Y', 'I', 'Yi', 'Y', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', 'KH', 'TS', 'CH',
            'SH',
            'SHCH', 'YU', 'YA', 'Y', 'YE', '_', '_', '_', '_', 'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y',
            'i',
            'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'Kh', 'Ts', 'Ch', 'Sh', 'Shch', 'Yu',
            'Aa',
            'y', 'Ye', '_', '_', '_', '_'))
        map_cyr_to_latin = {ord(src): dest for src, dest in zip(*table_symbols)}
        rx = re.compile(r"[^\w_]")
        return rx.sub('_', name.translate(map_cyr_to_latin))
    
    def make_folders(self, _dir, folder_list, folder_sep):
        for x in range(0, len(folder_list)):
            if not os.path.exists(f'{_dir}{folder_sep}{folder_list[x]}'):
                os.makedirs(f'{_dir}{folder_sep}{folder_list[x]}')
    
    def move_files(self, path, item_name, file_type, folder_name, base_path_to, folder_sep, files_type):
        check_exist_path = os.path.exists(f'{base_path_to}{folder_sep}{folder_name}{folder_sep}{item_name}')
        if file_type in files_type.get(folder_name) and not check_exist_path:
            path_from = f'{path}{folder_sep}{item_name}'
            to_path = f'{base_path_to}{folder_sep}{folder_name}{folder_sep}{item_name}'
            shutil.move(path_from, to_path)
    
    def find_files_and_sort(self, path, main_path, folder_list, folder_sep, files_type):
        for item_name in os.listdir(path):
            path_from = f'{path}{folder_sep}{item_name}'
            if item_name not in folder_list and os.path.isfile(path_from) and item_name != '.DS_Store':
                file_type = item_name.split('.')[-1]
                rem_suffix = item_name.removesuffix(f'.{file_type}')
                path_to_unpack = f'{main_path}{folder_sep}archives{folder_sep}{rem_suffix}'
                for folder_name in folder_list:
                    if folder_name != 'archives':
                        Sorter().move_files(path, item_name, file_type, folder_name, main_path, folder_sep, files_type)
                    elif file_type in files_type.get('archives') and not os.path.exists(path_to_unpack):
                        shutil.unpack_archive(path_from, path_to_unpack)
                        os.remove(path_from)
            elif item_name not in folder_list and os.path.isdir(path_from):
                Sorter().find_files_and_sort(path_from, main_path,folder_list, folder_sep, files_type)
    
    def rename_files_and_folders(self, path, folder_sep):
        for folder_item in os.listdir(path):
            path_to_folder = f'{path}{folder_sep}{folder_item}'
            path_after_normalize = f'{path}{folder_sep}{Sorter().normalize(folder_item)}'
            file_type = folder_item.split('.')[-1]
            rem_suffix = folder_item.removesuffix(f'.{file_type}')
            normalize_name = f'{Sorter().normalize(rem_suffix)}.{file_type}'
            if os.path.isfile(path_to_folder) and folder_item != '.DS_Store':
                shutil.move(path_to_folder, f'{path}{folder_sep}{normalize_name}')
            elif os.path.isdir(path_to_folder):
                shutil.move(path_to_folder, path_after_normalize)
                Sorter().rename_files_and_folders(path_after_normalize, folder_sep)
    
    def remove_empty_folders(self, path_abs, folder_list, folder_sep):
        walk = list(os.walk(path_abs))
        for path, folders, folders_items in walk[::-1]:
            folder_name = path.split(folder_sep)[-1]
            len_0 = len(os.listdir(path)) == 0 and folder_name not in folder_list
            len_1 = len(os.listdir(path)) == 1 and folder_name not in folder_list and '.DS_Store' in folders_items
            if len_0 or len_1:
                shutil.rmtree(path)
                
    def sort(self, _dir: str) -> None:
        
        folder_sep = "//" if platform == "win32" else "/"
        _dir = Path(_dir)
        main_path = _dir
        if not os.path.exists(main_path):
            print("No such directory.")
            return
        folder_list = ['images', 'documents', 'audio', 'video', 'archives']
        files_type = {
            'video': ['avi', 'mp4', 'mov', 'mkv'],
            'audio': ['mp3', 'ogg', 'wav', 'amr'],
            'images': ['jpeg', 'png', 'jpg', 'svg'],
            'archives': ['zip', 'gz', 'tar'],
            'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        }
        Sorter().make_folders(_dir, folder_list, folder_sep)
        Sorter().rename_files_and_folders(str(_dir), folder_sep)
        Sorter().find_files_and_sort(str(_dir), main_path, folder_list, folder_sep, files_type)
        Sorter().remove_empty_folders(_dir, folder_list, folder_sep)
        print('Sorted')
