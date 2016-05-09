class Constants(object):

    N_BOOT = 200
    UPDATE_EVERY = -1
    JOB = 1
    SEPARATOR = ' '
    COMPOSITE_KEY_SEPARATOR = ','
    ONLINE_UPDATE = 'WeightedMeanUpdater'
    BATCH_UPDATE = ''
    PRECISION = 1e3
    QUANTILE = 0.5
    MODEL = 'ElasticNet'
    TEST_FILE = None

    def __init__(self):
        pass
