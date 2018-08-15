from lib.services import AppService
from client.parsers import exclude_keys


def task_show_handler(service: AppService, namespace):
    if namespace.show_type == 'id':
        task = service.get_task_by_id(user_id=namespace.user_id,
                                      task_id=namespace.task_id)
        print(task)

    elif namespace.show_type == 'own':
        [print(x) for x in service.get_own_tasks(
            user_id=namespace.user_id)]

    elif namespace.show_type == 'inner':
        [print(x) for x in service.get_inner_tasks(
            user_id=namespace.user_id, task_id=namespace.parent_task_id)]

    elif namespace.show_type == 'access':
        [print(x) for x in service.get_available_tasks(
            user_id=namespace.user_id)]

    elif namespace.show_type == 'assigned':
        [print(x) for x in service.get_user_assigned_tasks(
            user_id=namespace.user_id)]

    elif namespace.show_type == 'repeat':
        [print(x) for x in service.get_generated_tasks(
            user_id=namespace.user_id)]

    elif namespace.show_type == 'repeatless':
        [print(x) for x in service.get_available_tasks(
            user_id=namespace.user_id) if x.repeat is None]


def task_handler(service: AppService, namespace):
    if namespace.action == 'create':
        task = service.create_task(user_id=namespace.user_id,
                                   name=namespace.name,
                                   description=namespace.description,
                                   start_date=namespace.start_date,
                                   end_date=namespace.end_date,
                                   parent_task_id=namespace.parent_task_id,
                                   priority=namespace.priority)
        print(task)

    elif namespace.action == 'show':
        task_show_handler(service, namespace)

    elif namespace.action == 'edit':
        args = exclude_keys(namespace)
        print(args)
        if not args:
            print('Nothing to update.')
        else:
            task = service.update_task(user_id=namespace.user_id,
                                       task_id=namespace.task_id,
                                       args=args)
            print('Updated task:', task)

    elif namespace.action == 'share':
        service.share_task(user_id=namespace.user_id,
                           user_receiver_id=namespace.user_receiver_id,
                           task_id=namespace.task_id)
        print(f'Task with ID={namespace.task_id} shared with user ID={namespace.user_receiver_id}')

    elif namespace.action == 'unshare':
        service.unshared(user_id=namespace.user_id,
                         user_receiver_id=namespace.user_receiver_id,
                         task_id=namespace.task_id)

        print(f'Task {namespace.task_id} unshared on {namespace.user_receiver_id}')

    elif namespace.action == 'assign':
        service.assign_user(user_id=namespace.user_id,
                            task_id=namespace.task_id,
                            user_receiver_id=namespace.user_receiver_id)

    elif namespace.action == 'set_subtask':
        service.add_subtask(user_id=namespace.user_id,
                            task_id=namespace.parent_task_id,
                            subtask_id=namespace.task_id)

    elif namespace.action == 'done':
        service.change_task_status(user_id=namespace.user_id,
                                   task_id=namespace.task_id,
                                   status='done',
                                   apply_on_subtasks=namespace.archive_subs)

    elif namespace.action == 'archive':
        service.change_task_status(user_id=namespace.user_id,
                                   task_id=namespace.task_id,
                                   status='archived',
                                   apply_on_subtasks=namespace.archive_subs)

    elif namespace.action == 'delete':
        service.delete_task(user_id=namespace.user_id,
                            task_id=namespace.task_id)
        print(f'Task with {namespace.task_id} ID deleted')


def folder_show_handler(service: AppService, namespace):

    if namespace.show_type == 'id':
        folder = service.get_folder_by_id(user_id=namespace.user_id,
                                          folder_id=namespace.folder_id)
        print('Folder name:', folder)
        if namespace.tasks:
            if folder.tasks:
                print('Folder tasks:')
                [print(x) for x in folder.tasks]
            else:
                print('Folder dont have any tasks')

    elif namespace.show_type == 'all':
        folders = service.get_all_folders(user_id=namespace.user_id)

        if not folders:
            print('You dont have folders')
            return

        if namespace.tasks:
            for folder in folders:
                print(folder)
                if folder.tasks:
                    for task in folder.tasks:
                        print(task)
        else:
            for folder in folders:
                print(folder)


def folder_handler(service: AppService, namespace):
    if namespace.action == 'create':
        folder = service.create_folder(user_id=namespace.user_id,
                                       name=namespace.name)
        print(folder)

    elif namespace.action == 'show':
        folder_show_handler(service, namespace)

    elif namespace.action == 'edit':
        try:
            folder = service.get_folder_by_name(namespace.user_id)
        except:
            print('Folder with such name already exist')
            return
        service.update_folder(folder_id=namespace.folder_id,
                              user_id=namespace.user_id,
                              args=exclude_keys(namespace))

    elif namespace.action == 'populate':

        service.populate_folder(user_id=namespace.user_id,
                                folder_id=namespace.folder_id,
                                task_id=namespace.task_id)

    elif namespace.action == 'unpopulate':

        service.unpopulate_folder(user_id=namespace.user_id,
                                  folder_id=namespace.folder_id,
                                  task_id=namespace.task_id)
        # folder = service.get_folder_by_id(user_id=namespace.user_id,
        #                                   folder_id=namespace.id)
        # task = folder.get_task_by_id(user_id=namespace.user_id,
        #                              task_id=namespace.task_id)
        # if task in folder.tasks:
        #     folder.tasks.remove(task)
        #     print(f'Task {task.id} no longer in {folder.name}')
        # else:
        #     print('Folder doesnt contain task with following id')
        # service.save_updates()


def print_repeats(repeat):
    ...


def repeat_show_handlers(service: AppService, namespace):
    if namespace.show_type == 'id':
        repeat = service.get_repeat_by_id(user_id=namespace.user_id,
                                          repeat_id=namespace.repeat_id)
        if namespace.tasks:
            ...  # TODO:

    elif namespace.show_type == 'all':
        repeats = service.get_all_repeats(user_id=namespace.user_id)

        #  TODO:


def repeat_handler(service: AppService, namespace):
    if namespace.action == 'create':

        repeat = service.create_repeat(user_id=namespace.user_id,
                                       period_amount=namespace.period_amount,
                                       period_Type=namespace.period_type,
                                       repetitions_amount=namespace.repeat_amount,
                                       end_date=namespace.end_date)
        print(repeat)

    elif namespace.action == 'show':

        repeat_show_handlers(service, namespace)

    elif namespace.action == 'edit':

        args = exclude_keys(namespace)
        if not args:
            print('Nothing to update')
            return

        service.update_repeat(repeat_id=namespace.repeat_id,
                              user_id=namespace.user_id,
                              args=args)

    elif namespace.action == 'delete':

        service.delete_repeat(user_id=namespace.user_id,
                              repeat_id=namespace.repeat_id)


def commands_handler(service: AppService, namespace):

    if namespace.entity == 'task':
        task_handler(service, namespace)

    elif namespace.entity == 'folder':
        folder_handler(service, namespace)

    elif namespace.entity == 'repeat':
        repeat_handler(service, namespace)
