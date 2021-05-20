import http
import os

import flask_restful.reqparse as reqparse
import flask_restful as flkrst
import pymongo

api = flkrst.Api()

contexts_parser = reqparse.RequestParser()
contexts_parser.add_argument("cpu_count", type=int)
contexts_parser.add_argument("cpu_frequency", type=int)
contexts_parser.add_argument("cpu_type", type=str)
contexts_parser.add_argument("cpu_vendor", type=str)
contexts_parser.add_argument("ram_tota", type=int)
contexts_parser.add_argument("machine_node", type=str)
contexts_parser.add_argument("machine_type", type=str)
contexts_parser.add_argument("machine_arch", type=str)
contexts_parser.add_argument("system_info", type=str)
contexts_parser.add_argument("python_info", type=str)
contexts_parser.add_argument("h", type=str)

sessions_parser = reqparse.RequestParser()
sessions_parser.add_argument("session_h", type=str)
sessions_parser.add_argument("run_date", type=str)
sessions_parser.add_argument("scm_ref", type=str)
sessions_parser.add_argument("descriptio", type=str)

metrics_parser = reqparse.RequestParser()
metrics_parser.add_argument("session_h", type=str)
metrics_parser.add_argument("context_h", type=str)
metrics_parser.add_argument("item_start_time", type=str)
metrics_parser.add_argument("item_path", type=str)
metrics_parser.add_argument("item", type=str)
metrics_parser.add_argument("item_variant", type=str)
metrics_parser.add_argument("item_fs_loc", type=str)
metrics_parser.add_argument("kind", type=str)
metrics_parser.add_argument("component", type=str)
metrics_parser.add_argument("total_time", type=float)
metrics_parser.add_argument("user_time", type=float)
metrics_parser.add_argument("kernel_time", type=float)
metrics_parser.add_argument("cpu_usage", type=float)
metrics_parser.add_argument("mem_usage", type=float)

MONGO_CONN_STRING = f"mongodb://" \
                    f"{os.environ.get('MONGO_INITDB_ROOT_USERNAME')}:" \
                    f"{os.environ.get('MONGO_INITDB_ROOT_PASSWORD')}@" \
                    f"{os.environ.get('MONGO_HOST')}:" \
                    f"{os.environ.get('MONGO_PORT')}"
MONGO_PYMON_DB = 'pymon'

mongo_client = pymongo.MongoClient(MONGO_CONN_STRING, maxPoolSize=200)
db = mongo_client[MONGO_PYMON_DB]


class PyMonContexts(flkrst.Resource):
    def get(self, hash):
        res = list(db.context.find({"h": hash}))
        if len(res) == 0:
            return '', http.HTTPStatus.NO_CONTENT
        else:
            res[0].pop('_id', None)
            body = {"contexts": res}
            return body, http.HTTPStatus.OK

    def post(self):
        # TODO(Vlad): Check if context already exists
        args = contexts_parser.parse_args()
        db.context.insert_one(args)
        return {'h': args["h"]}, http.HTTPStatus.CREATED


class PyMonSessions(flkrst.Resource):
    def get(self, hash):
        res = list(db.session.find({"session_h": hash}))
        if len(res) == 0:
            return '', http.HTTPStatus.NO_CONTENT
        else:
            res[0].pop('_id', None)
            body = {"sessions": res}
            return body, http.HTTPStatus.OK

    def post(self):
        # TODO(Vlad): Check if session already exists
        args = sessions_parser.parse_args()
        db.session.insert_one(args)
        return {'h': args["session_h"]}, http.HTTPStatus.CREATED


class PyMonMetrics(flkrst.Resource):
    def post(self):
        args = metrics_parser.parse_args()
        db.metrics.insert_one(args)
        return '', http.HTTPStatus.CREATED


api.add_resource(PyMonContexts, '/contexts/<string:hash>', '/contexts/')
api.add_resource(PyMonSessions, '/sessions/<string:hash>', '/sessions/')
api.add_resource(PyMonMetrics, '/metrics/')
