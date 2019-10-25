import os
import pathlib
import sys
import traceback

import cv2
import matplotlib.pyplot as plt
def TestRunner(folder_name, file_glob, solve, testdata, description, debug):
    """
        folder_name (str):
            Folder Name of test images

        file_glob (str): Glob selector for images, ignores ".ignore" extension

        solve (func):
            `solve(data, description)` Solves for 1 testcase

        testdata (func): `testdata(index, name, total)` Returns data for solve

        description (func): `description(index, name, total)` Returns desc for solve

        debug (bool): Defalut to False
    """
   
    class __test:
        def __init__(self, folder_name, file_glob, solve, testdata, description, debug):
            self.mshow = self.__pltshow(debug)
            self.folder_name = folder_name.strip("\\/")
            self.file_glob = file_glob
            self.solve = solve
            self.testdata = testdata
            self.description = description
            self.debug = debug

        def get_configuration(self):
            res = {}
            res['folder_name'] = self.folder_name
            res['file_glob'] = self.file_glob
            res['solve'] = self.solve
            res['testdata'] = self.testdata
            res['description'] = self.description 
            res['debug'] = self.debug
            return res

        class __pltshow:
            def __init__(self, debug):
                self.frames = []
                self.i = -1
                self.imgplot = None
                self.fig = None
                self.debug = debug
                self.grid_visible = False

            def next_frame(self, event=None):
                if event is not None and event.key in ['q', 's', 'f', 'escape', 'h', 'r', 'c', 'o']:
                    if event.key in ['q', 'escape']:
                        self.i = len(self.frames) - 1
                        plt.close()
                    return
                if event is not None and (isinstance(event.key, str) and event.key.rsplit("+", 1)[-1] == 'g'):
                    self.grid_visible = not self.grid_visible
                    plt.grid(self.grid_visible)
                
                if event is None or (isinstance(event.key, str) and event.key.rsplit("+", 1)[-1] in ['right']):
                    if self.i == len(self.frames) - 1:
                        plt.close()
                        return
                    while True:
                        self.i += 1
                        if self.i == len(self.frames):
                            plt.close()
                            return
                        if self.debug == True:
                            break
                        if self.frames[self.i][2] == False:
                            break
                    if self.imgplot is None:
                        self.imgplot = self.ax.imshow(self.frames[self.i][0], cmap=self.frames[self.i][3])
                        if self.frames[self.i] is not None:
                            self.fig.canvas.set_window_title(self.frames[self.i][1])
                        self.fig.tight_layout()
                        plt.show()
                    else:
                        self.imgplot.set_data(self.frames[self.i][0])
                        if self.frames[self.i] is not None:
                            self.fig.canvas.set_window_title(self.frames[self.i][1])
                        self.fig.tight_layout()
                        self.fig.canvas.draw()
                elif (isinstance(event.key, str) and event.key.rsplit("+", 1)[-1] in ['left']):
                    if self.i == -1:
                        plt.close()
                        return
                    while True:
                        self.i -= 1
                        if self.i == -1:
                            self.i += 1
                            return
                        if self.debug == True:
                            break
                        if self.frames[self.i][2] == False:
                            break
                    self.imgplot.set_data(self.frames[self.i][0])
                    if self.frames[self.i] is not None:
                        self.fig.canvas.set_window_title(self.frames[self.i][1])
                    self.fig.tight_layout()
                    self.fig.canvas.draw()

            def show(self, data, debug, title, cmap):
                # self.frames.append((data, title, debug, cmap))
                pass

            def finish(self):
                self.fig, self.ax = plt.subplots()
                self.fig.canvas.mpl_connect('key_press_event', self.next_frame)
                plt.grid(self.grid_visible)
                self.next_frame()

        def pp(self, *args, **kwargs):
            if not self.debug:
                return
            if 'i' in kwargs:
                print(f'\033[32m{kwargs["i"]} = \033[90m', *args, '\033[0m')
            else:
                print('\033[90m',*args,'\033[0m')

        def show(self, image, debug=False, title=None, cmap=None):
            if debug and self.debug == False:
                pass
            else:
                self.mshow.show(image, debug, title, cmap)

        def test(self):
            self.paths = pathlib.Path(self.folder_name).glob(self.file_glob)
            self.file_paths = filter(lambda x:x.is_file() and not x.name.endswith(".ignore") , self.paths)
            self.file_list = list(map(lambda x: os.fspath(x), self.file_paths))
            total = len(self.file_list)
            if total == 0:
                print(f'\033[32mNo test to run. \033[33m(Glob = {self.folder_name}/{self.file_glob})\033[0m')
                exit()
            for i, filename in enumerate(self.file_list, 1):
                try:
                    self.solve(self.testdata(i, filename, total), self.description(i, filename, total))
                except Exception as err:
                    print(f"\033[31m", sys.exc_info()[0].__name__, f"on file no {i} of {total} - \033[33m{filename}\033[35m")
                    print(getattr(err, 'message', str(err)), '\033[34m')
                    traceback.print_tb(err.__traceback__)
                    print("\033[0m")
            self.mshow.finish()

    t = __test(folder_name, file_glob, solve, testdata, description, debug)
    return t.show, t.pp, t.test, t.get_configuration()