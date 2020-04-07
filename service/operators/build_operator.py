import logging
import os, shutil

# Internal packages:
from service.handlers import BuilderFactory
from service.static import Request

logger = logging.getLogger(__name__)


def mark_success(transactionId: str, jar_location: str) -> dict:
    return {
        "transactionId": transactionId,
        "jar_location": jar_location
    }


def run_build(input_args) -> dict:
    logger.info(f"Build operation started for TransactionId: {input_args.transactionId}")
    builder = BuilderFactory(input_argss=input_args).get_builder()
    logger.info("Builder fetched!")
    logger.info(f"fetched builder: {type(builder)}")
    try:
        local_jar_location = builder.build()
        logger.info("Jar's build complete!")
        move_fat_jar_to_predefined_location(local_jar_location, input_args.fatJarLocation)
        logger.info(f"Jar's moved to predefined location {input_args.fatJarLocation}")
        builder.cleanup()
    except Exception as e:
        logger.error(f"Error in build process: {e}")
        raise e
    else:
        logger.info(f"Build operation finished for TransactionId: {input_args.transactionId}")
        return mark_success(input_args.transactionId, input_args.fatJarLocation)
    finally:
        pass


def move_fat_jar_to_predefined_location(src: str, dst: str):
    separator = os.path.sep
    dst_path_parts =dst.split(separator)
    dst_path = f"{separator}".join(dst_path_parts[0: len(dst_path_parts) - 1])

    # check if directory exists or not yet
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    shutil.move(src, dst)
