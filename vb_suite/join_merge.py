from vbench.benchmark import Benchmark
from datetime import datetime

common_setup = """from pandas_vb_common import *
"""

setup = common_setup + """
level1 = np.array([rands(10) for _ in xrange(10)], dtype='O')
level2 = np.array([rands(10) for _ in xrange(1000)], dtype='O')
label1 = np.arange(10).repeat(1000)
label2 = np.tile(np.arange(1000), 10)

key1 = np.tile(level1.take(label1), 10)
key2 = np.tile(level2.take(label2), 10)

shuf = np.arange(100000)
random.shuffle(shuf)
try:
    index2 = MultiIndex(levels=[level1, level2], labels=[label1, label2])
    index3 = MultiIndex(levels=[np.arange(10), np.arange(100), np.arange(100)],
                        labels=[np.arange(10).repeat(10000),
                                np.tile(np.arange(100).repeat(100), 10),
                                np.tile(np.tile(np.arange(100), 100), 10)])
    df_multi = DataFrame(np.random.randn(len(index2), 4), index=index2,
                         columns=['A', 'B', 'C', 'D'])
except:  # pre-MultiIndex
    pass

try:
    DataFrame = DataMatrix
except:
    pass

df = DataFrame({'data1' : np.random.randn(100000),
                'data2' : np.random.randn(100000),
                'key1' : key1,
                'key2' : key2})


df_key1 = DataFrame(np.random.randn(len(level1), 4), index=level1,
                    columns=['A', 'B', 'C', 'D'])
df_key2 = DataFrame(np.random.randn(len(level2), 4), index=level2,
                    columns=['A', 'B', 'C', 'D'])
"""

#----------------------------------------------------------------------
# DataFrame joins on key

join_dataframe_index_single_key_small = \
    Benchmark("df.join(df_key1, on='key1')", setup,
              name='join_dataframe_index_single_key_small')

join_dataframe_index_single_key_bigger = \
    Benchmark("df.join(df_key2, on='key2')", setup,
              name='join_dataframe_index_single_key_bigger')

join_dataframe_index_multi = \
    Benchmark("df.join(df_multi, on=['key1', 'key2'])", setup,
              name='join_dataframe_index_multi',
              start_date=datetime(2011, 10, 20))

#----------------------------------------------------------------------
# DataFrame joins on index



#----------------------------------------------------------------------
# Merges

#----------------------------------------------------------------------
# data alignment

setup = common_setup + """n = 1000000
# indices = Index([rands(10) for _ in xrange(n)])
def sample(values, k):
    sampler = np.random.permutation(len(values))
    return values.take(sampler[:k])
sz = 500000
rng = np.arange(0, 10000000000000, 10000000)
stamps = np.datetime64(datetime.now()).view('i8') + rng
idx1 = np.sort(sample(stamps, sz))
idx2 = np.sort(sample(stamps, sz))
ts1 = Series(np.random.randn(sz), idx1)
ts2 = Series(np.random.randn(sz), idx2)
"""
stmt = "ts1 + ts2"
series_align_int64_index = \
    Benchmark(stmt, setup,
              name="series_align_int64_index",
              start_date=datetime(2010, 6, 1), logy=True)

stmt = "ts1.align(ts2, join='left')"
series_align_left_monotonic = \
    Benchmark(stmt, setup,
              name="series_align_left_monotonic",
              start_date=datetime(2011, 3, 1), logy=True)
