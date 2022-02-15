import sys
from pathlib import Path
import shutil
import os
import re
import time
import asyncio
import aioshutil
from aiopath import AsyncPath

SORTING_DICT = {
    'archives': ('ZIP', 'GZ', 'TAR'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'images': ('JPEG', 'PNG', 'JPG', 'JFIF', 'SVG'),
}

TABLE_SYMBOLS = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ',
                 (
                     *(u'abvhgde'), 'ye', 'zh', *
                     (u'zyi'), 'yi', *(u'yklmnoprstuf'),
                     'kh', 'ts',
                     'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', *
                     (u'ABVHGDE'),
                     'Ye', 'Zh', *(u'ZYI'),
                     'Yi', *(u'YKLMNOPRSTUF'), 'KH', 'TS', 'CH', 'SH',
                     'SHCH', 'YU', 'YA', 'Y', 'YE', 'Y',
                     *(u'_' * 4)
                 )
                 )


async def recursive_sort_directory(path: Path, main_dir: Path):
    '''
         Recursive sort directory
    '''
    if await path.is_dir() and path.name not in SORTING_DICT.keys():
        async for element in path.iterdir():

            await recursive_sort_directory(element, main_dir)

    else:

        sort_file(path, main_dir)


def normalize(name: str):
    '''
        Transliterate cyrrylic symbols to latin
    '''
    map_cyr_to_latin = {ord(src): dest for src, dest in zip(*TABLE_SYMBOLS)}
    rx = re.compile(r"[^\w_]")
    return rx.sub('_', name.translate(map_cyr_to_latin))


def sort_file(path: Path, main_dir: Path):
    file_extension = path.name.split('.')[1]
    file_name = path.name.split('.')[0]

    for folder, extension in SORTING_DICT.items():
        if file_extension.upper() in extension:
            if main_dir.joinpath(folder).exists():
                shutil.move(
                    path.as_posix(),
                    main_dir.joinpath(folder).joinpath(
                        normalize(file_name)+'.'+file_extension)
                )
            else:
                os.mkdir(main_dir.joinpath(folder))
                shutil.move(
                    path.as_posix(),
                    main_dir.joinpath(folder).joinpath(
                        normalize(file_name)+'.'+file_extension)
                )


async def remove_empty_folders(path: Path):
    '''
        Recursively removes empty folders + renames folders using 'normalize function'
    '''
    if path.is_dir() and path.name not in SORTING_DICT.keys():

        for element in path.iterdir():
            if element.is_dir():
                shutil.move(
                    element,
                    element.parent.joinpath(normalize(element.name))
                )
                element = element.parent.joinpath(normalize(element.name))
                await remove_empty_folders(element)

        if not list(path.iterdir()):
            shutil.rmtree(path)


async def unpack_archives(path: Path):
    '''
        Checks if folder "archives" exists, then unpack archive + removes it
    '''
    archives_folder = path.joinpath('archives')

    if not archives_folder.exists():
        return

    for archive in archives_folder.iterdir():
        destination = archive.parent.joinpath(archive.name.split('.')[0])
        await aioshutil.unpack_archive(archive, destination)

        archive.unlink()


async def clean_folder_func():
    folder_path = sys.argv[1]

    if len(sys.argv) > 2:
        print('Too much arguments.')
        sys.exit()

    folder_path = AsyncPath(folder_path)
    main_dir = Path(folder_path)
    if not await folder_path.exists():
        print("Invalid path to folder. Restart script with correct 'path'.")
        sys.exit()

    await recursive_sort_directory(folder_path, main_dir)
    await remove_empty_folders(main_dir)
    await unpack_archives(main_dir)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(clean_folder_func())
    print('Function done in {:.4f} seconds'.format(time.time()-start_time))
