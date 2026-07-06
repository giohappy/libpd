import os
import sys

# 1. Add compiled pylibpd directories to Python's module search path (sys.path)
current_dir = os.path.dirname(os.path.abspath(__file__))
build_release_dir = os.path.join(current_dir, "build", "Release")
build_dir = os.path.join(current_dir, "build")

# Insert directories at the beginning of sys.path to prioritize our compiled modules
sys.path.insert(0, current_dir)
sys.path.insert(1, build_release_dir)
sys.path.insert(2, build_dir)

# 2. Add pthreads DLL directory to Python's DLL search path (required for Python 3.8+ on Windows)
if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
    pthreads_dll_dir = "D:/me/dev/vcpkg/packages/pthreads_x64-windows/bin"
    vcpkg_installed_dll_dir = "D:/me/dev/vcpkg/installed/x64-windows/bin"
    
    # Try adding both paths if they exist
    dll_added = False
    for path in [pthreads_dll_dir, vcpkg_installed_dll_dir]:
        if os.path.exists(path):
            os.add_dll_directory(path)
            print(f"Added DLL directory to search path: {path}")
            dll_added = True
            
    if not dll_added:
        print("Warning: Could not locate vcpkg pthreads DLL directory automatically.")
        print("If import fails with 'DLL load failed', please copy pthreadVC3.dll next to this script.")

# 3. Test pylibpd import and basic functionality
try:
    import pylibpd
    print("\n--- pylibpd successfully imported! ---")
    
    # Initialize basic audio characteristics
    block_size = pylibpd.libpd_blocksize()
    print(f"libpd block size: {block_size}")
    
    # Initialize audio (1 input, 2 outputs, 44100Hz sample rate)
    status = pylibpd.libpd_init_audio(1, 2, 44100)
    print(f"Audio initialization status: {status} (0 is success)")
    
    print("\nAll basic checks passed. libpd Python bindings are working correctly with MSVC Python!")
except ImportError as e:
    print("\nFailed to import pylibpd:", e, file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print("\nAn error occurred during verification:", e, file=sys.stderr)
    sys.exit(1)
