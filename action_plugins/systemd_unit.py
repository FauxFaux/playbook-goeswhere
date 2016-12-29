import os
from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.utils.hashing import checksum


class ActionModule(ActionBase):
    """
    Get the file copied to the remote machine before we need it
    """

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        source = self._task.args.get('src')
        dest = self._task.args.get('dest', None)

        if not dest:
            dest = '/etc/systemd/system/' + os.path.basename(source)

        try:
            source = self._find_needle('files', source)
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = str(e)
            return result

        source_full = self._loader.get_real_file(source)

        dest_status = self._execute_remote_stat(dest, all_vars=task_vars, follow=False, tmp=tmp)

        module_args = self._task.args.copy()

        if not dest_status['exists'] or checksum(source_full) != dest_status['checksum']:
            # cargo-culted
            remote_user = task_vars.get('ansible_ssh_user') or self._play_context.remote_user

            tmp = self._make_tmp_path(remote_user)
            tmp_source = os.path.join(tmp, 'source')
            self._transfer_file(source_full, tmp_source)
            module_args['src'] = tmp_source
        else:
            module_args['src'] = None

        module_args['dest'] = dest

        return self._execute_module(
            module_name='systemd_unit',
            module_args=module_args,
            tmp=tmp,
            task_vars=task_vars)
