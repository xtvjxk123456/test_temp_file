# coding:utf-8
import mmap
import contextlib


def replaceLine(origin, target, m):
    # replace以前绝对已经读取了line
    old_length = m.size()
    old_mtell = m.tell()
    if len(origin) < len(target):
        # need resize to larger
        m.resize(old_length + len(target) - len(origin))
        m.move(old_mtell + len(target) - len(origin), old_mtell, old_length - old_mtell)
    if len(origin) > len(target):
        m.move(old_mtell - len(origin) + len(target), old_mtell, old_length - old_mtell)
        m.resize(old_length - len(target) + len(origin))

    to_write = old_mtell - len(origin)
    if to_write < 0:
        to_write = 0
    m.seek(to_write)

    m.write(target)
    m.flush()


def run():
    f = r'E:\monster\library\assets\character\cBird\shd\mon_cBird_shd_v010_mma.ma'
    ma = open(f, 'r+')
    with contextlib.closing(mmap.mmap(ma.fileno(), 0, access=mmap.ACCESS_WRITE))as m:

        # m.readline()
        # m.readline()
        first = m.readline()
        replaceLine(first.decode('utf-8'), 'sfsdfsdfsdf\n', m)
        # ma.close()
        # with open(f, 'r+') as m:
        #     mm = mmap.mmap(m.fileno(),0, access=mmap.ACCESS_WRITE)
        #     mm.readline()
        #     first = mm.readline()
        #     replaceLine(first, '//di san hang \n', mm)
        #     mm.close()
