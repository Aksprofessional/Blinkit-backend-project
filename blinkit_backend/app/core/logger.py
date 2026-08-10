import logging

#basic logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

#name here is of that specific file where eroor is there.
logger = logging.getLogger(__name__)

#logging only for unexpected failures like Database crashed,Email service failed,Cloudinary failed,Commit failed
#not for buisness logic failures 