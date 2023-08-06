import os
import sys

# Apparently the more "modern" approach is to properly install your package
# before testing, which avoids this path hackery, but this is fine for now.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
