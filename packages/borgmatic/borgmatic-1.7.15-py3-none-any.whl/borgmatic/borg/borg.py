import logging

import borgmatic.commands.arguments
import borgmatic.logger
from borgmatic.borg import environment, flags
from borgmatic.execute import DO_NOT_CAPTURE, execute_command

logger = logging.getLogger(__name__)


REPOSITORYLESS_BORG_COMMANDS = {'serve', None}
BORG_SUBCOMMANDS_WITH_SUBCOMMANDS = {'key', 'debug'}
BORG_SUBCOMMANDS_WITHOUT_REPOSITORY = (('debug', 'info'), ('debug', 'convert-profile'), ())


def run_arbitrary_borg(
    repository_path,
    storage_config,
    local_borg_version,
    options,
    archive=None,
    local_path='borg',
    remote_path=None,
):
    '''
    Given a local or remote repository path, a storage config dict, the local Borg version, a
    sequence of arbitrary command-line Borg options, and an optional archive name, run an arbitrary
    Borg command on the given repository/archive.
    '''
    borgmatic.logger.add_custom_log_levels()
    lock_wait = storage_config.get('lock_wait', None)

    try:
        options = options[1:] if options[0] == '--' else options

        # Borg commands like "key" have a sub-command ("export", etc.) that must follow it.
        command_options_start_index = 2 if options[0] in BORG_SUBCOMMANDS_WITH_SUBCOMMANDS else 1
        borg_command = tuple(options[:command_options_start_index])
        command_options = tuple(options[command_options_start_index:])

        if borg_command and borg_command[0] in borgmatic.commands.arguments.ACTION_ALIASES.keys():
            logger.warning(
                f"Borg's {borg_command[0]} subcommand is supported natively by borgmatic. Try this instead: borgmatic {borg_command[0]}"
            )
    except IndexError:
        borg_command = ()
        command_options = ()

    if borg_command in BORG_SUBCOMMANDS_WITHOUT_REPOSITORY:
        repository_archive_flags = ()
    elif archive:
        repository_archive_flags = flags.make_repository_archive_flags(
            repository_path, archive, local_borg_version
        )
    else:
        repository_archive_flags = flags.make_repository_flags(repository_path, local_borg_version)

    full_command = (
        (local_path,)
        + borg_command
        + repository_archive_flags
        + command_options
        + (('--info',) if logger.getEffectiveLevel() == logging.INFO else ())
        + (('--debug', '--show-rc') if logger.isEnabledFor(logging.DEBUG) else ())
        + flags.make_flags('remote-path', remote_path)
        + flags.make_flags('lock-wait', lock_wait)
    )

    return execute_command(
        full_command,
        output_file=DO_NOT_CAPTURE,
        borg_local_path=local_path,
        extra_environment=environment.make_environment(storage_config),
    )
