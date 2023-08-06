from lib2 import __version__

class VersionUtil():
    @staticmethod
    def get_version():
        return __version__

if __name__ == "__main__":
    print(f"lib2 version: {VersionUtil.get_version()}")