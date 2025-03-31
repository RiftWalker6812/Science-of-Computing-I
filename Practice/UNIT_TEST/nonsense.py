import sys
import os

# Calculate the path: go up two levels from UNIT_TEST/ to Science-of-Computing-I/
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the Librarys directory to sys.path
sys.path.append(os.path.join(base_path, 'Librarys'))

from RiftLib import Reverse_Int

x = Reverse_Int(123)
print(str(x))
