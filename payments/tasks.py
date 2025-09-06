from celery import shared_task

@shared_task
def test_celery():
    print("Выполняется test_celery!")
    return "Задача успешно выполнена"