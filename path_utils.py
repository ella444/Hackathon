import pathlib

class PathUtils:

    @staticmethod
    def get_dirs(path):
        p = pathlib.Path(path)
        return [x.name for x in p.iterdir() if x.is_dir()]


if __name__ == '__main__':
    print(PathUtils.get_dirs("./data"))
