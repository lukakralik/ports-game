import os
import unittest

os.environ["DATABASE_URL"] = "sqlite://"

if __name__ == "__main__":
    unittest.main(verbosity=2)
