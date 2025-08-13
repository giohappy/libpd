## Building Python bindings with MSVC

### Build
Assuming VS 2022 C++ and 

1. Assuming we're in `D:\music\dev\pd`
2. `git clone --recursive `https://github.com/giohappy/libpd.git` and switch to the python_msvc branch that contains the patches to `setup.py`
3. cd libpd
4. `git clone --recursive https://github.com/GerHobbelt/pthread-win32.git`
5. Open the VS Command prompt
6. `msbuild pthread-win32/windows/VS2022/pthread_lib.2022.vcxproj /p:Configuration=RELEASE /p:Platform=x64`
7. `cmake -S . -B build -G "Visual Studio 17 2022" -A x64 -DPD_MULTI=OFF -DPD_BUILD_C_EXAMPLES=ON -DPTHREADS_LIB="D:\music\dev\pd\libpd\pthread-win32\windows\VS2022\bin\DEBUG-Unicode-64bit-x64\pthread_static_lib.lib" -DPTHREADS_INCLUDE_DIR=pthread-win32/`
8. cd `python`
8. `python setup.py build_ext --inplace`

We get `pylibpd.py` inside `D:\music\dev\pd\libpd\python`

### Test
1. `python -m venv venv`
2. `pip install pyaudio, pygame, numpy`
3. `cd ../samples/python`
4. `python pygame_fun_test.py`
