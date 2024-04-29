# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

if __name__ == "__main__":
    num_1, num_2 = input("num_1: "), input("num_2: ")
    try:
        num_1 = int(num_1)
        num_2 = int(num_2)
        print(f"{num_1 + num_2}")
    except ValueError:
        print(f"{num_1 + num_2}")
