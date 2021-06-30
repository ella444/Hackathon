import pathlib

class Utils:

    @staticmethod
    def get_dirs(path):
        p = pathlib.Path(path)
        return [x.name for x in p.iterdir() if x.is_dir()]

    @staticmethod
    def get_files(path, suffix='.csv'):
        p = pathlib.Path(path)
        return [x.name for x in p.iterdir() if x.is_file()]

    @staticmethod
    def get_session(path, time_const_min=30):
        return ['ses1', 'ses2']

if __name__ == '__main__':
    print(Utils.get_dirs("./data"))
