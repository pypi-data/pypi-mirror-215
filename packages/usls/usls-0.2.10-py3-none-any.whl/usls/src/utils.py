import cv2
from pathlib import Path
import numpy as np
import rich
import shutil
import argparse
import os
from tqdm import tqdm
import sys
import random
import time
import logging
import glob
import re
import rich
from rich.console import Console
from datetime import datetime
import contextlib
import numpy as np
from dataclasses import dataclass
from typing import Union, List, Dict, Optional
from PIL import ExifTags, Image, ImageOps
import hashlib
from loguru import logger as LOGGER
import uuid
import urllib.request



CONSOLE = Console()
IMG_FORMAT = ('.jpg', '.jpeg', '.png', '.bmp')
LABEL_FORMAT = ('.txt', '.xml', '.yaml', '.csv')
VIDEO_FORMAT = ('.mp4', '.flv', '.avi', '.mov')
ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FEAT_WEIGHTS_URL = 'https://github.com/jamjamjon/assets/releases/download/usls/fe-224.onnx'


def download_from_url(url, saveout, prefix=''):

    # check saveout 
    if Path(saveout).exists() and Path(saveout).is_file():
        # print(f'{saveout} is already exists, return None.')
        return saveout
    else:
        # urllib.request.urlretrieve(str(url), filename=str(saveout))
        with urllib.request.urlopen(url) as source, open(saveout, "wb") as output:
            with tqdm(
                desc='downloading',
                total=int(source.info().get("Content-Length")),
                ncols=100,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as loop:
                while True:
                    buffer = source.read(8192)
                    if not buffer:
                        break
                    output.write(buffer)
                    loop.update(len(buffer))

        # print(f'{saveout} downloaded!')
        return saveout


def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_md5(f):
    m = hashlib.md5(open(f,'rb').read())
    return m.hexdigest()


def gen_random_string(length):
    return ''.join(random.choices(ASCII_LETTERS, k=length))


def get_common_files(
        directory,
        *,
        fmt=None,
        sort_=True
    ):

    # file list
    f_list = list()
    for x in Path(directory).iterdir():
        if fmt is None:  # get all files, hidden file excluded.
            if str(x).startswith('.'):   # hidden file, leave it
                continue
            elif x.suffix == '':   # no suffix
                if x.is_dir():
                    f_list.append(x)    # dir, append
                else:
                    continue
            else:
                f_list.append(x)    # has suffix, append
        else:  # get specific format file
            if x.suffix in fmt:
                f_list.append(x)


    if sort_:
        f_list.sort(key=natural_sort)    

    return f_list


def verify_images(path, output_dir):
    _check_again = True  # flag

    # PIL check 1st, and restore corrupt JPEG
    try: 
        with Image.open(path) as im:
            im.verify()   # PIL image quality check

            # jpg & jpeg corrupt check
            if im.format.lower() in ('jpeg', 'jpg'):
                with open(path, "rb") as f:
                    f.seek(-2, 2)
                    if f.read() != b'\xff\xd9':     # corrupt JPEG
                        ImageOps.exif_transpose(Image.open(path)).save(path, 'JPEG', subsampling=0, quality=100)
                        CONSOLE.log(f"Corrupt JPEG restored and saved | {path}")
    except OSError:
        CONSOLE.log(f"PIL verify failed! | {path}")
        shutil.move(str(path), str(output_dir))
        _check_again = False  # set flag
        # integrity = False
        return False


    # opencv check again
    if _check_again:
        try:
            if cv2.imread(str(path)) is None:  # get md5 of each image
                shutil.move(str(path), str(output_dir))
                return False
        except Exception as e:
            CONSOLE.log(f"opencv exceptions: {e} | {path}")
            return False

    return True



def natural_sort(x, _pattern=re.compile('([0-9]+)'), mixed=True):
    return [int(_x) if _x.isdigit() else _x for _x in _pattern.split(str(x) if mixed else x)]




# img_list & label_list, relative path
def load_img_label_list(img_dir, label_dir, img_format, info=True):
    image_list = [x for x in Path(img_dir).iterdir() if x.suffix in img_format]
    label_list = list(Path(label_dir).glob("*.txt"))
    
    if info:
        rich.print(f"[green]> Images count: {len(image_list)}")
        rich.print(f"[green]> Labels count: {len(label_list)}")
        

    return image_list, label_list



# img_path => label_path(txt)
def get_corresponding_label_path(img_path, output_dir):
    label_name = Path(img_path).stem + '.txt'
    saveout = Path(output_dir) / label_name 
    return str(saveout)




class TIMER(contextlib.ContextDecorator):

    def __init__(self, prefix='Inspector', verbose=True):
        self.prefix = prefix
        self.verbose = verbose


    def __enter__(self):
        self.t0 = time.time()
        return self


    def __exit__(self, type, value, traceback):
        self.duration = time.time() - self.t0
        if self.verbose:
            print(f"[{self.prefix}] --> {(time.time() - self.t0) * 1e3:.2f} ms.")


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = func(*args, **kwargs)
            if self.verbose:
                print(f"[{self.prefix}] --> {(time.time() - t0) * 1e3:.2f} ms.")

            return ret
        return wrapper




class Palette:
    """colors palette"""

    def __init__(self, shuffle=False):
        _hex_colors = [
            '33FF00', '9933FF', 'CC0000', 'FFCC00', '99FFFF', '3300FF',
            'FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', 
            '1A9334', '00D4BB', '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', 
            '520085', 'CB38FF', 'FF95C8', 'FF37C7', '#F0F8FF', '#4682B4', '#0000CD', '#9932CC',  
            '#FFB6C1', '#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585',  
            '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3',   
            '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', 
            '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', 
            '#87CEFA', '#87CEEB', '#00BFFF', '#808080', '#696969', '#000000', '#DA70D6', '#D8BFD8', 
            '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E1FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', 
            '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFAA', '#00FA9A', '#F5FFFA',  
            '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32', '#00FF00', '#228B22',  
            '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#6B8E23', '#FAFAD2', '#FFFFF0', '#FFFFE0',  
            '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#FFFAF0',  
            '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887',
            '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', 
            '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', 
            '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', 
            '#191970', '#9932CC', '#00CED1', '#2F4F4F', '#C0C0C0', '#A9A9A9', '#CD5C5C', '#FF0000',
            '#FFA07A', '#FF7F50', '#FFE4C4', '#FF8C00', '#FDF5E6', '#F5DEB3', '#FFFF00', '#808000',
            '#008000', '#006400', '#00FF7F', '#3CB371', '#4B0082',
        ]
        
        # shuffle color 
        if shuffle:
            random.shuffle(_hex_colors)

        self.palette = [self.hex2rgb(c) if c.startswith('#') else self.hex2rgb('#' + c) for c in _hex_colors]
        self.n = len(self.palette)


    def __call__(self, i, bgr=False):    
        """ int -> rgb color """    
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod  
    def hex2rgb(h):
        """
        int('CC', base=16) hex -> 10
        RGB的数值 = 16 * HEX的第一位 + HEX的第二位
        RGB: 92, 184, 232 
        92 / 16 = 5余12 -> 5C
        184 / 16 = 11余8 -> B8
        232 / 16 = 14余8 -> E8
        HEX = 5CB8E8
        """
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))



def smart_path(path='', *, exist_ok=False, sep='-', mkdir=False, method=0):
    # Increment file or directory path

    # random string in currnet path
    if path == '':
        if method == 0:
            _ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            path = Path.cwd() / (''.join(random.choices(_ASCII_LETTERS, k=8)))
        elif method == 1:
            path = Path.cwd() / str(uuid.uuid4())
        elif method == 2:
             path = Path.cwd() / datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = Path(path)  # os-agnostic

    # make increment
    if path.exists() and not exist_ok:
        path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')

        # increment path
        for n in range(2, 9999):
            p = f'{path}{sep}{n}{suffix}'  
            if not os.path.exists(p):  # non-exist will break
                break
        path = Path(p)

        # path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')
        # dirs = glob.glob(f"{path}{sep}*")  # similar paths
        # matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        # i = [int(m.groups()[0]) for m in matches if m]  # indices
        # n = max(i) + 1 if i else 2  # increment number
        # path = Path(f"{path}{sep}{n}{suffix}")  # increment path

    # make dir directly
    if mkdir:
        path.mkdir(parents=True, exist_ok=True)  # make directory


    return path






class USLS:

	def __init__(
		self, 
		name="usls"
		# *, 
	):
		self.name = name
		self._ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


	def _is_hidden(self, p):
		"""Checking if hidden file or directory."""
		return True if re.search(os.sep + '\.', str(p)) else False 


	def inspect(
		self,
		directory: str,
		*,
		fmt: List[str] = [],
		recursive: bool = True,
		include_hidden: bool = False,
		case_sensitive: bool = False,
		verbose: bool = True
	) -> (List, Dict):
		"""Summary of a directory."""

		# error checking
		if not Path(directory).is_dir():
			raise TypeError(f'Type of {Path(directory)} should be directory, not {type(directory)}')
			sys.exit()

		# saveout
		fs, mapping, ds = list(), dict(), list()
		# nf, nd, nhf, nhd = 0, 0, 0, 0  # num_file, num_dir, num_hidden_file, num_hidden_dir
		nt = 0 # number of total

		# glob
		with CONSOLE.status("[b]Loading...", spinner='flip') as _:  # status spinner
			for x in Path(directory).glob('**/*' if recursive else '*'):   # generator, not using tqdm
				nt += 1 	# count
				x = x.resolve() 	# use abs path
				
				if not include_hidden:  
					if self._is_hidden(x):    # if not show hidden
						continue
				
				if x.is_dir():   # is dir 
					ds.append(str(x))
					mapping.setdefault('directories', []).append(x)
				
				if not x.is_file():  # not valie file
					continue

				# saveout
				if (x.suffix if case_sensitive else x.suffix.lower()) in fmt or len(fmt) == 0:  # empty means every type
					fs.append(str(x))
					if x.suffix == '':   # no suffix file (only cope with last suffix)
						mapping.setdefault(x.stem, []).append(x)
					else:
						mapping.setdefault(x.suffix[1:] if case_sensitive else x.suffix[1:].lower(), []).append(x)

		# info
		if verbose:
			nd, nf = len(ds), len(fs)
			no = nt - nf - nd
			s = f"> Find {nf} files, {nd} directories"
			if no > 0:
				s += f", {no} others (other format file | hidden files | hidden directories)."
			elif no == 0:
				s += '.'
			elif no < 0:
				raise ValueError(f"> ValueError: number of other can not be smaller than 0")
			CONSOLE.print(s) 	# info
		
		return fs, ds, mapping



	def rename(
		self,
		directory, 
		*,
		with_prefix: str = '',
		with_num: bool = False,
		with_znum: bool = False,
		with_random: bool = False,
		with_uuid: bool = False,
		bits_random: int = 16,
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # No need to change
		include_hidden: bool = False,  # Hidden files should not be renamed!
		with_dir: bool = False,  # rename dir at the same time
		recursive: bool = False,  # Not recursive
		verbose: bool = True

	):
		"""Rename sub-dirs or files within directory"""

		# check ways, only one will work
		if not any((with_znum, with_num, with_random, with_uuid)):
			rich.print(f'> Attention: No method selected. Using [b cyan i]random[/b i cyan] strings default.')
			with_random = True

		# error checking
		if sum((with_znum, with_num, with_random, with_uuid)) > 1:
			raise ValueError(
				f'Methods selected too much at the same time:'
				f'\n\twith_znum: {with_znum}'
				f'\n\twith_num: {with_num}'
				f'\n\twith_random: {with_random}'
				f'\n\twith_uuid: {with_uuid}'
			)

		# glob files & directories
		f_list, d_list, _ = self.inspect(
			directory,
			recursive=recursive,  # false 
			fmt=fmt,  # []
			case_sensitive=case_sensitive, # false
			include_hidden=include_hidden,  # false
			verbose=verbose
		)

		# counting file
		if with_dir:
			f_list += d_list

		# uuid4 & random
		if with_uuid or with_random:
			sets_string = set()

			# gen uuid4/random string
			while len(sets_string) != len(f_list):
				sets_string.add(str(uuid.uuid4()) if with_uuid else ''.join(random.choices(self._ASCII_LETTERS, k=bits_random)))

			# rename
			for x, x_ in tqdm(zip(f_list, sets_string), desc='renaming', total=len(f_list)):
				x = Path(x)
				x.rename(x.with_stem(x_))


		# with num & znum & random letters
		if with_num or with_znum or with_prefix:

			# method with prefix
			if with_prefix:
				for x in tqdm(f_list, desc='renaming', total=len(f_list)): 
					x = Path(x)
					x.rename(x.with_stem(with_prefix + '-' + x.stem))
			else:  # make sure aligned
				for x in tqdm(f_list, desc='alignment', total=len(f_list)):
					x = Path(x)
					x.rename(x.with_stem('j1a2m3j4a5m6j7o8n9' + '-' + x.stem))        

			# method with num & znum
			if with_num or with_znum:

				# laod again
				f_list, d_list, _ = self.inspect(
					directory,
					recursive=recursive,
					fmt=fmt,
					case_sensitive=case_sensitive,
					include_hidden=include_hidden,
					verbose=verbose
				)

				if with_dir:
					f_list += d_list

				# rename
				idx = 0
				for x in tqdm(f_list, desc='renaming', total=len(f_list)):
					x = Path(x)
					x.rename(x.with_stem(str(idx) if with_num else str(idx).zfill(len(str(len(f_list))))))
					idx += 1


	def combine(
		self,
		directory_i: str,
		*,
		directory_o: str = 'output-conbined',
		move: bool = False,
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # false
		include_hidden: bool = False,  # false! Hidden files should not be combined!
		recursive: bool = True,  # true
		verbose: bool = True
	):

		# dir checking
		if not Path(directory_i).is_dir():
			raise TypeError(f'Type of {Path(directory_i)} should be directory, not {type(directory_i)}')

		# check saveout directory
		saveout_dir = Path(directory_o)
		if not saveout_dir.exists():
			saveout_dir.mkdir()
		else:
			CONSOLE.print(
				f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
			)
			sys.exit()	

		# glob
		f_list, d_list, _ = self.inspect(
			directory_i,
			fmt=fmt,
			case_sensitive=case_sensitive,  # false
			include_hidden=include_hidden,  # false
			recursive=recursive,  # true
			verbose=verbose
		)

		# combining
		if len(f_list) == 0:
			CONSOLE.print(
				f'[red]Error[/red] -> Files Not Found! Go check out '
				f'directory_i: [u]{Path(directory_i).resolve()}[/u]' 
				# f'fmt: {fmt} (empty means all)'
			)
			saveout_dir.rmdir() 	# remove saveout directory
			sys.exit()
		else:

			_method = 'move' if move else 'copy'
			for d in tqdm(f_list, desc=f"Combining [{_method}]", total=len(f_list)):

				# cut to reletive
				for i, x in enumerate(Path(d).parts):
					if Path(directory_i).name == x:
						d_ = '-'.join(Path(d).parts[i:])
						break

				# s = d.replace(os.path.sep, '-')
				# des_path = saveout_dir.resolve() / s 
				# print(f'd_: {d_}')
				des_path = saveout_dir.resolve() / d_

				# copy or move
				if move:  
					shutil.move(str(Path(d).resolve()), str(des_path))
				else:
					shutil.copy(str(Path(d).resolve()), str(des_path))
		CONSOLE.print(f"> Saved at: [u green]{saveout_dir.resolve()}")   # saveout log



	# def _check_image_integrity(self, path) -> (bool, Optional[str]):
	# 	"""check single image's integrity."""
	# 	_check_again = True  # flag
		
	# 	# PIL check 1st, and restore corrupt JPEG
	# 	try: 
	# 		with Image.open(str(path)) as im:
	# 			im.verify()   # PIL image quality check
	# 			if im.format.lower() in ('jpeg', 'jpg'): # jpeg checking & restore 
	# 				with open(path, "rb") as f:
	# 					f.seek(-2, 2)
	# 					if f.read() != b'\xff\xd9':     # corrupt JPEG
	# 						ImageOps.exif_transpose(Image.open(path)).save(path, 'JPEG', subsampling=0, quality=100)
	# 						CONSOLE.print(f"> Corrupt JPEG restored automatically: {path}")
	# 	except OSError:
	# 		_check_again = False  # set flag
	# 		return False, f"PIL verify failed! | {path}"

	# 	# opencv check again
	# 	if _check_again:
	# 		try:
	# 			if cv2.imread(str(path)) is None:  
	# 				return False, f"Image can not be read by OpenCV | {path}"
	# 		except Exception as e:
	# 			return False, f"OpenCV exceptions: {e} | {path}"
	# 	return True, None



	# def image_sanitizer(
	# 	self, 
	# 	directory_i, 
	# 	directory_o='output-deprecated',
	# 	fmt: List[str]=[],  # Default: all type files + dir, lower-case
	# 	case_sensitive: bool=False,   # No need to change
	# 	include_hidden: bool=False,  # Do not modify!
	# 	recursive: bool=True,  # No need to modify!
	# ):
		
	# 	has_deprecated = False  # flag

	# 	# check saveout directory
	# 	saveout_dir = Path(directory_o)
	# 	if not saveout_dir.exists():
	# 		saveout_dir.mkdir()
	# 	else:
	# 		CONSOLE.print(
	# 			f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
	# 		)
	# 		sys.exit()	

	# 	# glob
	# 	with CONSOLE.status("[b]Loading files...", spinner='grenade') as status:
	# 		f_list, _, _ = self.inspect(
	# 			directory_i,
	# 			fmt=fmt,
	# 			case_sensitive=case_sensitive,  # false
	# 			include_hidden=include_hidden,  # false
	# 			recursive=recursive  # true
	# 		)

	# 	# sanitize
	# 	for f in tqdm(f_list, desc=f"sanitizing", total=len(f_list)):
	# 		if not self._check_image_integrity(f)[0]:
	# 			has_deprecated = True
	# 			shutil.move(str(f), str(saveout_dir))

	# 	# check saveout dir
	# 	if not has_deprecated:
	# 		Path(saveout_dir).rmdir() 	# rmdir




	# def cleanup(self):
	# 	# clean up dir
	# 	...

