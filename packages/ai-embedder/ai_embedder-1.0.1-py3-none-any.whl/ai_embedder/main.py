import argparse
import os
import sys

import pywintypes
from win32com.client import GetActiveObject, Dispatch


def _parse_input():
    parser = argparse.ArgumentParser(
        prog="AI Link Embedder",
        description="This script takes .ai files and save them with linked files embedded"
    )
    parser.add_argument("dictionary", help="Directory with input .ai files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan for .ai files recursively")
    parser.add_argument("-o", "--override", action="store_true", help="Override resulting .ai is it exists")
    parser.add_argument("-d", "--dest", help="Directory where resulting .ai files will be saved to")
    parser.add_argument("-p", "--prefix", default="Prefix to be added to resulting .ai filename")
    parser.add_argument("-s", "--suffix", default="Suffix to be added to resulting .ai filename")
    return parser.parse_args()


def _get_files_with_extension(recursive, directory, extension):
    file_list = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    file_list.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.endswith(extension):
                file_list.append(os.path.join(directory, file))
    return file_list


def _apply_suffix_and_prefix(file, prefix, suffix):
    filename = f"{prefix}{os.path.basename(file).split('.')[0]}{suffix}.ai"
    return os.path.join(os.path.dirname(file), filename)


def _save_ai_with_embedded_links(app, src, dest):
    # Open File
    doc_ref = app.Open(src)

    # Save with EmbedLinkedFiles
    save_options = Dispatch("Illustrator.IllustratorSaveOptions")
    save_options.EmbedLinkedFiles = True
    doc_ref.SaveAs(dest, save_options)

    # Close without save message
    doc_ref.Close(2)


def run():
    args = _parse_input()

    # Try to attach or run Adobe Illustrator
    try:
        app = GetActiveObject("Illustrator.Application")
    except pywintypes.com_error:
        app = Dispatch("Illustrator.Application")

    app.userInteractionLevel = -1  # DONTDISPLAYALERTS

    ai_files = _get_files_with_extension(args.recursive, args.dictionary, ".ai")
    if args.dest is not None:
        ai_files = list(filter(lambda ai_file: not ai_file.startswith(args.dest), ai_files))
        dest = args.dest
    else:
        dest = args.dictionary

    skipped = 0

    for idx, ai_file in enumerate(ai_files):
        dest_file = _apply_suffix_and_prefix(os.path.join(dest, os.path.basename(ai_file)), args.prefix, args.suffix)
        if args.override or not os.path.isfile(dest_file):
            try:
                _save_ai_with_embedded_links(app, ai_file, dest_file)
            except Exception as e:
                print(f"\nFailed to process: {ai_file}", file=sys.stderr)
                raise e
        else:
            skipped += 1
        print(f"\rProcessed: {idx + 1}/{len(ai_files)} "
              f"({'{:.2f}'.format((idx + 1) * 100 / len(ai_files))}%), skipped: {skipped}", end="")
    print()
