from ckan.lib.celery_app import celery

@celery.task(name = "ksext.echofunction")
def echo( message ):
    print message
