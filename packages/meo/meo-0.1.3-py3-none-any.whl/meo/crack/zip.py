from pyzipper import ZipFile
import asyncio
from tqdm.asyncio import tqdm
from itertools import permutations
import multiprocessing
import itertools
import gc
import weakref
from tqdm.asyncio import tqdm

PWD_SEED = b"1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+-=[{}]\|;:,<.>/?'\" "
PWD_SEED_SIMPLE = b'1234567890qwertyuiopasdfghjklzxcvbnm'

def try_open_zip(zfile: ZipFile, pwd: bytes):
    assert isinstance(zfile, ZipFile) and isinstance(pwd, bytes)
    try:
        mem = zfile.filelist[0].filename
        with zfile.open(mem, pwd=pwd) as f:
            if f.seek(1):
                return True
    except ValueError as e:
        raise e
    except:
        return False
    
def guess_number_pwd(path, start=0, end=1e99, step=1):
    zfile = ZipFile(path)
    for number in tqdm(range(start, end, step)):
        pwd = str(number).encode("utf8")
        if try_open_zip(zfile, pwd):
            return pwd
    return None
            
def key_permution(seed, size):
    for k in permutations(seed, size):
        yield bytes(k)

def key_generator(start=None, end=None, seed=PWD_SEED):
    n_size = 1 if start is None else max(int(start), 1)
    if end is None:
        while True:
            for k in key_permution(seed, n_size):
                yield k, n_size
            n_size += 1
    else:
        end = int(end)
        while True:
            if n_size <= end:
                for k in key_permution(seed, n_size):
                    yield k, n_size
            else:
                return StopIteration()
            n_size += 1

async def guess_async_by_seed(path, min_length=None, max_length=None, seed=PWD_SEED):
    zfile = ZipFile(path)

    async def block(pwd):
        if try_open_zip(zfile, pwd):
            return pwd
        return False
    
    with tqdm(key_generator(min_length, max_length, seed=seed)) as bar:
        async for pwd, _ in bar:
            if await block(pwd):
                return pwd
    return None

def guess_pwd_normal_by_seed(path, min_length=None, max_length=None, seed=PWD_SEED):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(guess_async_by_seed(path, min_length, max_length, seed))
    loop.run_until_complete(future)
    pwd = future.result()
    return pwd

def __guess_step(path, *pwds: bytes):
    zfile = ZipFile(path)
    for pwd in pwds:
        if try_open_zip(zfile, pwd):
            return pwd
    del pwds
    return False

def guess_in_multiprocess_by_seed(path, min_length=None, max_length=None, n_processes=8, slice_size=500, seed=PWD_SEED, progressbar=False):
    pool = multiprocessing.Pool(n_processes)
    it = key_generator(min_length, max_length, seed=seed)
    manager = multiprocessing.Manager()
    info = manager.dict()
    info['key'] = None
    if progressbar:
        bar = tqdm(mininterval=0.25)
    def cb(re):
        if progressbar:
            bar.update(slice_size)
        if re:
            info['key'] = re
            pool.terminate()
    while True:
        for _ in range(n_processes):
            try:
                pwds = itertools.islice(it, 0, slice_size)
                if pwds := list(pwds):
                    pwds, char_sizes = list(zip(*pwds))
                    char_size = char_sizes[-1]
                    pool.apply_async(__guess_step, (path, *pwds), callback=cb, error_callback=print)
                    del pwds
                    del char_sizes
                else:
                    pool.close()
                    pool.join()
                    pool.terminate()
                    return info['key']
            except Exception as e:
                if e.args[0] == 'Pool not running':
                    return info['key']
                else:
                    raise e
        if progressbar:
            bar.set_postfix({
                "char": char_size
            }, refresh=False)
        gc.collect()

async def guess_async_by_book(path, book: list[bytes]):
    zfile = ZipFile(path)
    
    async def block(pwd):
        if try_open_zip(zfile, pwd):
            return pwd
        return False
    
    with tqdm(book) as bar:
        async for pwd in bar:
            if await block(pwd):
                return pwd
    return None

def guess_pwd_normal_by_book(path, book: list[bytes]):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(guess_async_by_book(path, book))
    loop.run_until_complete(future)
    pwd = future.result()
    return pwd

def guess_in_multiprocess_by_book(path, book:list, n_processes=8, slice_size=500, progressbar=False):
    pool = multiprocessing.Pool(n_processes)
    manager = multiprocessing.Manager()
    info = manager.dict()
    info['key'] = None
    if progressbar:
        bar = tqdm(mininterval=0.25)
    def cb(re):
        if progressbar:
            bar.update(slice_size)
        if re:
            info['key'] = re
            pool.terminate()
    while True:
        for _ in range(n_processes):
            try:
                pwds = itertools.islice(book, 0, slice_size)
                if pwds := list(pwds):
                    pool.apply_async(__guess_step, (path, *pwds), callback=cb, error_callback=print)
                    del pwds
                else:
                    pool.close()
                    pool.join()
                    pool.terminate()
                    return info['key']
            except Exception as e:
                if e.args[0] == 'Pool not running':
                    return info['key']
                else:
                    raise e
        gc.collect()
        
        
class ZipCracker:

    def __init__(self, path) -> None:
        self.path = path

    def only_number(self):
        return guess_number_pwd(self.path)
    
    async def by_seed_async(self, seed=PWD_SEED, min_length=None, max_length=None):
        return await guess_async_by_seed(self.path, min_length, max_length, seed=seed)
    
    def by_seed(self, seed=PWD_SEED, min_length=None, max_length=None):
        return guess_pwd_normal_by_seed(self.path, min_length, max_length, seed=seed)
    
    def by_seed_mp(self, seed=PWD_SEED, min_length=None, max_length=None, n_processes=8, slice_size=500, progressbar=False):
        return guess_in_multiprocess_by_seed(self.path, min_length, max_length, n_processes, slice_size, seed=seed, progressbar=progressbar)

    def by_book(self, book: list[bytes]):
        return guess_pwd_normal_by_book(self.path, book=book)
    
    def by_book_mp(self, book: list[bytes], n_processes=8, slice_size=500, progressbar=False):
        return guess_in_multiprocess_by_book(self.path, book=book, n_processes=n_processes, slice_size=slice_size, progressbar=progressbar)


if __name__ == '__main__':
    zguess = ZipCracker("./examples/data/flag.zip")
    # zguess = ZipCracker("./test/flag.zip", seed=PWD_SEED_SIMPLE)
    # pwd = zguess.by_seed(PWD_SEED_SIMPLE)
    # pwd = zguess.by_seed_mp(n_processes=13, slice_size=1000, progressbar=True, min_length=1, max_length=3, seed=PWD_SEED_SIMPLE)
    # print(pwd)
    
    from codedict import Codes
    k = zguess.by_book(map(lambda x: x.encode('utf8'), Codes.all_in()))
    print(k)
    print(len(list(map(lambda x: x.encode('utf8'), Codes.all_in()))))