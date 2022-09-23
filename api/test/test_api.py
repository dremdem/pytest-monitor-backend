import http
import unittest
import unittest.mock as mock

import mongomock

import api
import app


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.test_client = app.create_app().test_client()
        self.mongo_client = mongomock.MongoClient('localhost', 27017)
        self.context_get_hash = 'qwerty'
        self.context_post = {
            "cpu_count": 8,
            "cpu_frequency": 2600,
            "cpu_type": "i386",
            "cpu_vendor": "Intel(R) Core(TM) i7-4960HQ CPU @ 2.60GHz",
            "ram_tota": None,
            "machine_node": "localcomp.local",
            "machine_type": "x86_64",
            "machine_arch": "64bit",
            "system_info": "Darwin - 19.6.0",
            "python_info": "3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27)"
                           "[Clang 6.0 (clang-600.0.57)]",
            "h": "e951f91e787401e0159e3708173ab691"
        }
        self.session_get_hash = 'asdfg'
        self.session_post = {
            "session_h": "c2c5b0d5d3c799ce9fc174451609f47f",
            "run_date": "2021-05-07T01:16:59.032413",
            "scm_ref": "2cc4cdda54450ca99a340c2c309f1fc19579d78b",
            "description": None}

        self.metric_post = {
            "session_h": "c2c5b0d5d3c799ce9fc174451609f47f",
            "context_h": "e951f91e787401e0159e3708173ab691",
            "item_start_time": "2021-05-07T01:18:12.303720",
            "item_path": "test1",
            "item": "test_sleep1",
            "item_variant": "test_sleep1",
            "item_fs_loc": "test1.py",
            "kind": "function",
            "component": None,
            "total_time": 1.2086470127105713,
            "user_time": 0.002227359999999956,
            "kernel_time": 0.003211335999999995,
            "cpu_usage": 0.004499821654134455,
            "mem_usage": 1.41015625}

    def test_contexts_get(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            response = self.test_client.get(f"/contexts/{self.context_get_hash}")
            assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_contexts_post(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            response = self.test_client.post("/contexts/",
                                             data=self.context_post)
            assert response.status_code == http.HTTPStatus.CREATED
            # Check if context exists in MongoDB
            contexts = list(api.db.context.find({"h": self.context_post['h']}))
            assert len(contexts), 1

    def test_sessions_get(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            response = self.test_client.get(f"/sessions/{self.session_get_hash}")
            assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_session_post(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            response = self.test_client.post("/sessions/",
                                             data=self.session_post)
            assert response.status_code == http.HTTPStatus.CREATED
            # Check if session exists in MongoDB
            sessions = list(api.db.session.
                            find({"session_h": self.session_post['session_h']}))
            assert len(sessions), 1

    def test_metrics_post(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            response = self.test_client.post("/metrics/",
                                             data=self.metric_post)
            assert response.status_code == http.HTTPStatus.CREATED
            # Check if metric exists in MongoDB
            metrics = list(api.db.metrics.
                           find({"session_h": self.metric_post['session_h'],
                                 "item": self.metric_post['item']}))
            assert len(metrics), 1

    def test_integration_full(self):
        with mock.patch.object(api, "db",
                               self.mongo_client[api.MONGO_PYMON_DB]):
            # Cleanup db.
            api.db.context.drop()
            api.db.session.drop()
            api.db.metrics.drop()
            # Emulate full chain of requests.
            response = self.test_client.get(f"/contexts/{self.context_post['h']}")
            assert response.status_code == http.HTTPStatus.NO_CONTENT
            response = self.test_client.post("/contexts/",
                                             data=self.context_post)
            assert response.status_code == http.HTTPStatus.CREATED
            response = self.test_client.\
                get(f"/sessions/{self.session_post['session_h']}")
            assert response.status_code == http.HTTPStatus.NO_CONTENT
            response = self.test_client.post("/sessions/",
                                             data=self.session_post)
            assert response.status_code == http.HTTPStatus.CREATED
            response = self.test_client.post("/metrics/",
                                             data=self.metric_post)
            assert response.status_code == http.HTTPStatus.CREATED


