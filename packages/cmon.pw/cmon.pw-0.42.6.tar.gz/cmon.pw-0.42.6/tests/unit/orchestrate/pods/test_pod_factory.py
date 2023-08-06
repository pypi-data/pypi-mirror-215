import pytest
from hubble.executor.hubio import HubIO

from cmon.orchestrate.pods.factory import PodFactory
from cmon.parsers import set_pod_parser


@pytest.mark.parametrize(
    'uses', ['cmonai+docker://cmon.pw/DummyExecutor']
)
def test_container_pod(mocker, monkeypatch, uses):
    mock = mocker.Mock()

    def _mock_pull(self):
        return 'docker://cmonhub/dummy_executor'

    monkeypatch.setattr(HubIO, 'pull', _mock_pull)

    args = set_pod_parser().parse_args(['--uses', uses])
    pod = PodFactory.build_pod(args)
    assert pod.args.uses == 'docker://cmonhub/dummy_executor'
    assert pod.name == 'ContainerPod'
