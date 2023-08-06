import logging

from flexmock import flexmock

from borgmatic.borg import borg as module

from ..test_verbosity import insert_logging_mock


def test_run_arbitrary_borg_calls_borg_with_flags():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
    )


def test_run_arbitrary_borg_with_log_info_calls_borg_with_info_flag():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo', '--info'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )
    insert_logging_mock(logging.INFO)

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
    )


def test_run_arbitrary_borg_with_log_debug_calls_borg_with_debug_flag():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo', '--debug', '--show-rc'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )
    insert_logging_mock(logging.DEBUG)

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
    )


def test_run_arbitrary_borg_with_lock_wait_calls_borg_with_lock_wait_flags():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    storage_config = {'lock_wait': 5}
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(()).and_return(
        ('--lock-wait', '5')
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo', '--lock-wait', '5'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config=storage_config,
        local_borg_version='1.2.3',
        options=['break-lock'],
    )


def test_run_arbitrary_borg_with_archive_calls_borg_with_archive_flag():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo::archive'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
        archive='archive',
    )


def test_run_arbitrary_borg_with_local_path_calls_borg_via_local_path():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg1', 'break-lock', 'repo'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg1',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
        local_path='borg1',
    )


def test_run_arbitrary_borg_with_remote_path_calls_borg_with_remote_path_flags():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(
        ('--remote-path', 'borg1')
    ).and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo', '--remote-path', 'borg1'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['break-lock'],
        remote_path='borg1',
    )


def test_run_arbitrary_borg_passes_borg_specific_flags_to_borg():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'list', 'repo', '--progress'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['list', '--progress'],
    )


def test_run_arbitrary_borg_omits_dash_dash_in_flags_passed_to_borg():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'break-lock', 'repo'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['--', 'break-lock'],
    )


def test_run_arbitrary_borg_without_borg_specific_flags_does_not_raise():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').never()
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg',),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=[],
    )


def test_run_arbitrary_borg_passes_key_sub_command_to_borg_before_repository():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'key', 'export', 'repo'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['key', 'export'],
    )


def test_run_arbitrary_borg_passes_debug_sub_command_to_borg_before_repository():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'debug', 'dump-manifest', 'repo', 'path'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['debug', 'dump-manifest', 'path'],
    )


def test_run_arbitrary_borg_with_debug_info_command_does_not_pass_borg_repository():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').never()
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'debug', 'info'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['debug', 'info'],
    )


def test_run_arbitrary_borg_with_debug_convert_profile_command_does_not_pass_borg_repository():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module.flags).should_receive('make_repository_flags').never()
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'debug', 'convert-profile', 'in', 'out'),
        output_file=module.borgmatic.execute.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.run_arbitrary_borg(
        repository_path='repo',
        storage_config={},
        local_borg_version='1.2.3',
        options=['debug', 'convert-profile', 'in', 'out'],
    )
