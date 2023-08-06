from cmon.schemas.gateway import schema_gateway
from cmon.schemas.helper import _cli_to_schema
from cmon_cli.export import api_to_dict

_schema_flow_with = _cli_to_schema(
    api_to_dict(),
    ['flow', 'gateway'],
    allow_addition=False,
    description='The config of Flow, unrecognized config arguments will be applied to all Deployments',
)['Cmon::Flow']

schema_flow = {
    'Cmon::Flow': {
        'properties': {
            'with': _schema_flow_with,
            'jtype': {
                'description': 'The type of Cmon object (Flow, Executor).\n'
                'A Flow is made up of several sub-tasks, and it manages the states and context of these sub-tasks.\n'
                'The input and output data of Flows are Documents.',
                'type': 'string',
                'default': 'Flow',
                'enum': ['Flow'],
            },
            'version': {
                'description': 'The YAML version of this Flow.',
                'type': 'string',
                'default': '\'1\'',
            },
            'executors': {
                'description': 'Define the steps in the Flow.\n'
                'A Deployment is a container and interface for one or multiple Pods that have the same properties.',
                'type': 'array',
                'items': {'$ref': '#/definitions/Cmon::Deployment'},
                'minItems': 1,
            },
            'gateway': schema_gateway['Cmon::Gateway'],
        },
        'type': 'object',
        'additionalProperties': False,
        'required': ['jtype', 'executors'],
    }
}
