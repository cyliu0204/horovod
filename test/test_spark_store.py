import os
import unittest
import warnings


import mock

from horovod.spark.common.store import HDFSStore
from horovod.spark.common.store import S3Store

class SparkStoreTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(SparkStoreTests, self).__init__(*args, **kwargs)
        self.maxDiff = None
        warnings.simplefilter('module')


    @mock.patch('horovod.spark.common.store.HDFSStore._get_filesystem_fn')
    def test_sync_hdfs_store(self, mock_get_fs_fn):
        mock_fs = mock.Mock()
        mock_get_fs_fn.return_value = lambda: mock_fs

        hdfs_root = '/user/test/output'
        store = S3Store(hdfs_root)
        store.get_local_output_dir_fn()
        run_id = 'run_001'
        get_local_output_dir = store.get_local_output_dir_fn(run_id)
        sync_to_store = store.sync_fn(run_id)
        run_root = store.get_run_path(run_id)

        def touch(fname, times=None):
            with open(fname, 'a'):
                os.utime(fname, times)

        with get_local_output_dir() as local_dir:
            touch(os.path.join(local_dir, 'a.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'a.txt'), mock.ANY)

            touch(os.path.join(local_dir, 'b.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'b.txt'), mock.ANY)

            subdir = os.path.join(local_dir, 'subdir')
            os.mkdir(subdir)
            touch(os.path.join(subdir, 'c.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'subdir/c.txt'), mock.ANY)

            touch(os.path.join(local_dir, 'a.txt'), (1330712292, 1330712292))
            touch(os.path.join(local_dir, 'b.txt'), (1330712292, 1330712292))
            assert mock_fs.upload.call_count == 3

            sync_to_store(local_dir)
            assert mock_fs.upload.call_count == 5


    @mock.patch('horovod.spark.common.store.HDFSStore._get_filesystem_fn')
    def test_sync_s3_store(self, mock_get_fs_fn):
        mock_fs = mock.Mock()
        mock_get_fs_fn.return_value = lambda: mock_fs

        s3_root = '/user/test/output'
        store = (s3_root)

        run_id = 'run_001'
        get_local_output_dir = store.get_local_output_dir_fn(run_id)
        sync_to_store = store.sync_fn(run_id)
        run_root = store.get_run_path(run_id)

        def touch(fname, times=None):
            with open(fname, 'a'):
                os.utime(fname, times)

        with get_local_output_dir() as local_dir:
            touch(os.path.join(local_dir, 'a.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'a.txt'), mock.ANY)

            touch(os.path.join(local_dir, 'b.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'b.txt'), mock.ANY)

            subdir = os.path.join(local_dir, 'subdir')
            os.mkdir(subdir)
            touch(os.path.join(subdir, 'c.txt'), (1330712280, 1330712280))
            sync_to_store(local_dir)
            mock_fs.upload.assert_called_with(os.path.join(run_root, 'subdir/c.txt'), mock.ANY)

            touch(os.path.join(local_dir, 'a.txt'), (1330712292, 1330712292))
            touch(os.path.join(local_dir, 'b.txt'), (1330712292, 1330712292))
            assert mock_fs.upload.call_count == 3

            sync_to_store(local_dir)
            assert mock_fs.upload.call_count == 5
