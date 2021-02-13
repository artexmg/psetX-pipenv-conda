from unittest import TestCase
from tempfile import TemporaryDirectory
import tempfile
from typing import ContextManager, Union
from contextlib import contextmanager
import os

class FakeFileFailure(IOError):
    pass

@contextmanager
def atomic_write(file: Union[str, os.PathLike], mode:str='w', as_file:bool = True, **kwargs) -> ContextManager:

    # Fist validates datatypes
    assert isinstance(file,(str,type(os.path))),'file datatype expected str or pathLike'
    assert isinstance(mode,str),'mode datatype expected to be string'
    assert isinstance(as_file,bool), 'as_file datatype expected to be bool'
    
    # ---
    #    retrieves target file name, depending on the input type:
    #      string 
    #      os.PathLike 
    # ---
    if isinstance(file,type(os.path)):
        target_file = file.name
    else:
        target_file = file
    # # if target file is not fully qualified, then its path is set to local directory
    # if isinstance(file,str):
    #     target_file = os.path.join(os.getcwd(),target_file)

    # if target file already exists, then it raises exception
    assert not os.path.exists(target_file), f'target file {target_file} already exists'
    
    # creates a temporary file 
    tmp_file = tempfile.NamedTemporaryFile(mode=mode,delete=False)
    try:
        yield tmp_file 

    except IOError:
        tmp_file.close()
        if os.path.exists(target_file): os.remove(target_file)
        if os.path.exists(target_file): os.remove(target_file)
        raise
    else:
        #close and then rename temporary file to target file    
        os.rename(tmp_file.name,target_file)
        tmp_file.close()
    # finally:
    #     # in case the temporary file was not renamed before 
    #     # (due to a crash), then it is removed
    #     if os.path.exists(tmp_file.name): os.remove(tmp_file.name)
        


if __name__ == "__main__":

    file = '/var/folders/h5/jh7gfnvs3gb6j6dvltzq15dr0000gn/T/tmpdt4ch5cq'
    file = 'amg.txt'

    # with atomic(file) as file:
    #     print(f'tmp file {file.name}')
 
    class AtomicWriteTests(TestCase):
        def test_atomic_failure(self):
            """Ensure that file does not exist after failure during write"""

            with TemporaryDirectory() as tmp:
                fp = os.path.join(tmp, "asdf.txt")

                with self.assertRaises(FakeFileFailure):
                    with atomic_write(fp, "w") as f:
                        tmpfile = f.name
                        assert os.path.exists(tmpfile)
                        raise FakeFileFailure()

                assert not os.path.exists(tmpfile)
                assert not os.path.exists(fp)
                print('teto')

    a = AtomicWriteTests()

    a.test_atomic_failure()

    
    