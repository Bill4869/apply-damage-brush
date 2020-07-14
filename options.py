import argparse
import os


class BaseOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        self.parser.add_argument('--target', help='path to target image')
        self.parser.add_argument('--map', help='path to map image if available')
        self.parser.add_argument('--brushesRoot', help='path to brush folder')
        self.parser.add_argument('--output', default='./result/', help='path to output results')
        self.parser.add_argument('--gridScale', type=int, default=1, help='grid scale')
        self.parser.add_argument('--usePoisson', default=False, action='store_true' help='use poisson or not')

        self.parser.add_argument('--sigma', type=int, default=20, help='sigma for gaussian filter')
        self.parser.add_argument('--threshold', type=int, default=20, help='the bigger threshold is, the bigger probability area in map gets')


        # self.parser.add_argument('--gaussianWeight', type=int, default=, help='grid scale')

        
    def parse(self):
        self.opt = self.parser.parse_args()

        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        return self.opt

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

