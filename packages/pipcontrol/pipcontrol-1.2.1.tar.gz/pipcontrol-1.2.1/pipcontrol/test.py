if __name__ == "__main__":
    import sys

    argv_str = ""
    for argv in sys.argv:
        argv_str += argv + " "
    print(f"print test with argv : {argv_str}")
