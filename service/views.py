from flask_restful import Resource, reqparse
from flask_api import status
import logging

# Internal packages:
from service.operators import run_build
from service.static import Request
from service import api, app

logger = logging.getLogger(__name__)
abst_request_parser = reqparse.RequestParser(bundle_errors=True)
abst_request_parser.add_argument('transactionId', type=str, required=True)


class SubmitBuild(Resource):
    def post(self):
        submit_parser = abst_request_parser.copy()
        submit_parser.add_argument('build_type',
                                   choices=('maven', 'gradle', 'sbt'),
                                   help='Bad choice - allowed values [maven, gradle, sbt]: {error_msg}',
                                   location='json', required=True)
        submit_parser.add_argument('sourcePath', type=str, location='json', required=True)
        submit_parser.add_argument('fatJarLocation', type=str, location='json', required=True)
        args = submit_parser.parse_args()
        try:
            logger.info(f"Arguments parsed: {args}")
            #request = Request(input_args=args)
            logger.info(f"Request built! Running build (transaction: {args.transactionId})...")
            app.logger.info(f"POST request received! Arguments: {args}")
            result = run_build(input_args=args)
            return dict(result), status.HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def get(self):
        return {"message": "Helloooo ;)"}, status.HTTP_200_OK


class Recompile(Resource):
    def post(self):
        # Maybe not necessary....
        recompile_parser = abst_request_parser.copy()
        recompile_parser.add_argument('build_type', type=str, location='json', required=True)
        recompile_parser.add_argument('git_url', type=str, location='json', required=True)
        recompile_parser.add_argument('branch', type=str, location='json', required=True)
        recompile_parser.add_argument('run_script_path', type=str, location='json', required=True)
        args = recompile_parser.parse_args()


api.add_resource(SubmitBuild, "/build")
api.add_resource(Recompile, "/recompile")
