from ckan.lib.celery_app import celery

@celery.task(name = "NAME.echofunction")
def echo( message ):
    print message