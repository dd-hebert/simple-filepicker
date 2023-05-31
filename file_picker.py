# -*- coding: utf-8 -*-
"""
Simple utilities to view directories and pick files from the terminal.

Created on Fri May 27 2023

@author: David Hebert
"""

import os
import pdb

class FilePicker:
    """
    A FilePicker object.

    Contains methods to pick and view files and directories from the console.

    Attributes
    ----------
    file_list : list
        A list of tuples containing a subfolder name ``file_list[x][0]`` and
        a list of files in each subfolder ``file_list[x][1]``.

    """

    def __init__(self, root, file_ext):
        """
        Create a FilePicker object.

        Parameters
        ----------
        root : string
            A file path to a directory containing folders and files.
        file_ext : string
            The file extension of interest (e.g., '.jpeg').

        Returns
        -------
        None.

        """
        self.file_list = []
        self.root = root
        self.ext = file_ext

        # Get names of subfolders containing files
        # in the :attr:`~FilePicker.root` directory.
        for path, subdirs, _ in os.walk(self.root):
            for name in subdirs:
                rel_path = os.path.join(os.path.relpath(path, root), name)
                # Each folder gets stored as a tuple.
                # The 1st value is the folder name.
                # The 2nd value is a list of files.
                self.file_list.append((rel_path, []))
                for file in os.listdir(os.path.join(path, name)):
                    if file.endswith(self.ext):
                        self.file_list[-1][1].append(file)
                # Pop if folder contains no files
                if self.file_list[-1][1] == []:
                    self.file_list.pop(-1)

        # Handle files directly in the root directory (no subfolder).
        self.file_list.append((self.root, []))
        for file in os.listdir(self.root):
            if file.endswith(self.ext):
                self.file_list[-1][1].append(file)
        # Pop if no files direcly in the root directory
        if self.file_list[-1][1] == []:
            self.file_list.pop(-1)

    def pick_file(self):
        """
        Pick a file interactively from the terminal.

        Returns
        -------
        string
            Returns the path of the chosen file relative to the root directory.

        """

        def print_folders_in_root():
            # Print list of folders in root directory
            print(f'\n{self.root}')
            max_digits = len(str(len(self.file_list)))
            for index, entry in enumerate(self.file_list):
                extra_spacing = max_digits - len(str(index + 1))
                spacing = ' ' * (4 + extra_spacing)
                print(f'[{index + 1}]{spacing}{entry[0]}')

        def get_folder_choice():
            # Get user folder choice
            user_folder = input('\nSelect a folder: ')
            accepted_range = range(1, len(self.file_list) + 1)

            if user_folder in ['q', 'Q']:
                return None
            elif user_folder.isnumeric() is False or int(user_folder) not in accepted_range:
                print_folders_in_root()
                print('\nInvalid selection. Input a folder number (shown in brackets)',
                      'or q to quit.')
                return get_folder_choice()
            else:
                folder_index = int(user_folder) - 1
                folder_name = self.file_list[folder_index][0]

                return folder_index, folder_name

        def print_files_in_folder(folder_index, folder_name):
            # Print list of files in user selected folder
            max_digits = len(str(len(self.file_list[folder_index][1])))
            spacing = ' ' * (6 + max_digits)
            print(f'\n{spacing}{folder_name}:')
            for index, file in enumerate(self.file_list[folder_index][1]):
                extra_spacing = max_digits - len(str(index + 1))
                spacing = ' ' * (4 + extra_spacing)
                if index < len(self.file_list[folder_index][1]) - 1:
                    print(f'[{index + 1}]{spacing}├───{file}\t')
                else:
                    print(f'[{index + 1}]{spacing}└───{file}\t')

        def get_file_choice(folder_index, folder_name):
            # Get user file choice
            user_file = input('\nSelect a file: ')
            accepted_range = range(1, len(self.file_list[folder_index][1]) + 1)

            if user_file in ['q', 'Q']:
                return None
            elif user_file in ['b', 'B']:
                self.pick_file()
            elif user_file.isnumeric() is False or int(user_file) not in accepted_range:
                print_files_in_folder(folder_index, folder_name)
                print('\nInvalid selection. Input a file number (shown in brackets)',
                      'or q (quit), b (back).')
                return get_file_choice(folder_index, folder_name)
            else:
                file_index = int(user_file) - 1
                file_name = self.file_list[folder_index][1][file_index]

                return file_name

        def print_selection(folder_name, file_name):
            print('┏' + '┅' * (len(file_name) + 17) + '┓')
            print(f'┇ File selected: {file_name} ┇')
            print('┗' + '┅' * (len(file_name) + 17) + '┛')

            # Get file path
            if folder_name == 'root':
                file_path = os.path.join(file_name)
            else:
                file_path = os.path.join(folder_name, file_name)

            return file_path

        def file_picker_loop():
            print_folders_in_root()
            folder_choice = get_folder_choice()
            if folder_choice is not None:
                folder_index, folder_name = folder_choice
                print_files_in_folder(folder_index, folder_name)
                file_choice = get_file_choice(folder_index, folder_name)
                if file_choice is not None:
                    return print_selection(folder_name, file_choice)
            return self.pick_file()

        return file_picker_loop()

    def tree(self):
        """
        Print the ``root directory`` file tree to the console.

        Returns
        -------
        None. Prints a file tree.

        """
        print(self.root)
        for index, entry in enumerate(self.file_list):
            if index < len(self.file_list) - 1:
                print(f'├───{entry[0]}')
                for i, file in enumerate(entry[1]):
                    if i < len(entry[1]) - 1:
                        print(f'│   ├───{file}\t')
                    else:
                        print(f'│   └───{file}\t')
            else:
                print(f'└───{entry[0]}')
                for i, file in enumerate(entry[1]):
                    if i < len(entry[1]) - 1:
                        print(f'    ├───{file}\t')
                    else:
                        print(f'    └───{file}\t')

if __name__ == '__main__':
    fp = FilePicker(r'H:\Documents\Lab Notebook', '.KD')

    output = fp.pick_file2()
