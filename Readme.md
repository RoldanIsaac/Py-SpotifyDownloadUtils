# Python Batch Uncompress & Rename Scripts

This repository contains Python scripts to **batch extract compressed files** and **rename folders** in a directory.

---

## Scripts

1. **`uncompress.py`**

   - Extracts `.zip`, `.tar`, `.tar.gz`, `.tgz`, and `.rar` files.
   - Deletes original compressed files after extraction.
   - Logs all operations in `extraction_log.txt`.

2. **`rename_folders.py`**

   - Recursively removes a given string from all folder names in a directory.
   - Can be run independently or after `uncompress.py`.

3. **`main.py`**
   - Master script to run `uncompress.py` and then `rename_folders.py` in sequence.
   - Can pass parameters like the target folder and string to remove.

---

## Requirements

- Python 3.7+
- Python packages:

  ```bash
  pip install rarfile
  ```

- For .rar files, you need the UnRAR executable:
  Windows

1. Download the command-line version of UnRAR from Rarlab.
2. Extract UnRAR.exe to a folder, e.g., C:\Program Files\UnRAR\.
3. Add the folder to your PATH environment variable or set it in the script:

```python
import rarfile
rarfile.UNRAR_TOOL = r"C:\Program Files\UnRAR\UnRAR.exe"
```

- Without UnRAR, .rar files will be skipped and the script will continue with other formats.

## Notes

- The scripts log all actions in extracted_files/extraction_log.txt.
- .rar extraction requires UnRAR; other formats work out of the box.
- Make sure the scripts are in the same folder if using main.py.

## License

MIT License
