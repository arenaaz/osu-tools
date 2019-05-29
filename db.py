import datetime as dt
import struct
'''
General osu! db util methods
'''
def read_bool(f):
    '''Returns a 1-byte osu! db Boolean.'''
    return bool(struct.unpack('?', f.read(1))[0])

def read_byte(f):
    '''Returns a osu! db Byte.'''
    return struct.unpack('b', f.read(1))[0]

def read_short(f):
    '''Returns a 2-byte osu! db Short.'''
    return struct.unpack('h', f.read(2))[0]

def read_int(f):
    '''Returns a 4-byte osu! db Int.'''
    return struct.unpack('i', f.read(4))[0]

def read_long(f):
    '''Returns a 8-byte osu! db Long.'''
    return struct.unpack('q', f.read(8))[0]

def read_single(f):
    '''Returns a 4-byte osu! db Single.'''
    return struct.unpack('f', f.read(4))[0]

def read_double(f):
    '''Returns a 8-byte osu! db Double.'''
    return struct.unpack('d', f.read(8))[0]

def read_datetime(f):
    '''Returns a 8-byte osu! db DateTime.'''
    ticks = read_long(f)  # .Net ticks
    return dt.datetime(1, 1, 1) + dt.timedelta(microseconds = ticks/10)

def read_string(f):
    '''Returns an osu! db String of variable length.
    
    String has three parts; a single byte which will be either 0x00, indicating that the next two parts are not present, or 0x0b (decimal 11), indicating that the next two parts are present. If it is 0x0b, there will then be a ULEB128, representing the byte length of the following string, and then the string itself, encoded in UTF-8.
    '''
    # part 1: indicator byte - 0x00 = next two parts are not present, or 0x0b = next two parts are present
    indicator = f.read(1)
    if indicator == b'\x0b':
        # part 2: ULEB128 - representing the byte length of the following string
        byte_len = get_uleb128(f)
        # part 3: string
        return str(f.read(byte_len), 'utf-8')
    elif indicator == b'\x00':
        return ''
    else:
        return

def get_uleb128(f):
    '''Returns a ULEB128 integer.'''
    value = 0
    for i in range(0,5):
        b = f.read(1)[0]
        tmp = b & 0x7f
        value = tmp << (i * 7) | value
        if (b & 0x80) != 0x80:
            break
    if i == 4 and (tmp & 0xf0) != 0:
        print("parse a error uleb128 number")
        return -1
    return value

class CollectionDB:
    
    def __init__(self, file):
        self.version = read_int(file)
        print('version:', self.version)

        # read no. of collections
        self.coll_count = read_int(file)
        print('no. of collections:', self.coll_count)
        
        # collections
        self.collections = {}
        for _ in range(self.coll_count):
            coll = Collection(file)
            self.collections[coll.name] = coll

class Collection:
    
    def __init__(self, file):

        # read name
        self.name = read_string(file)
        print('collection name:', self.name)
        # read no. of beatmaps in collection
        self.beatmap_count = read_int(file)
        print('no. of beatmaps:', self.beatmap_count)

        self.beatmap_md5s = []
        for b in range(self.beatmap_count):
            # read MD5
            md5 = read_string(file)
            self.beatmap_md5s.append(md5)
            print(f'beatmap#{b+1} MD5: {md5}')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
