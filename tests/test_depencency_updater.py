from unittest.mock import Mock

from baby_steps import given, then, when

from fresh_deps import DependencyUpdater, GitLabAPI


def test_dependency_updater():
    with given:
        gitlab_api = Mock(GitLabAPI)

    with when:
        dependency_updater = DependencyUpdater(gitlab_api)

    with then:
        assert dependency_updater
