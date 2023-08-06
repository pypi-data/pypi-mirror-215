def get_full_schema() -> dict:
    """Get full schema
    :return: the full schema for Cmon core as a dict.
    """
    from cmon import __version__
    from cmon.importer import IMPORTED
    from cmon.schemas.deployment import schema_deployment
    from cmon.schemas.executor import schema_all_executors
    from cmon.schemas.flow import schema_flow
    from cmon.schemas.gateway import schema_gateway
    from cmon.schemas.meta import schema_metas

    definitions = {}
    for s in [
        schema_gateway,
        schema_all_executors,
        schema_flow,
        schema_metas,
        schema_deployment,
        IMPORTED.schema_executors,
    ]:
        definitions.update(s)

    return {
        '$id': f'https://api.cmon.pw/schemas/{__version__}.json',
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'description': 'The YAML schema of Cmon objects (Flow, Executor).',
        'type': 'object',
        'oneOf': [{'$ref': '#/definitions/Cmon::Flow'}]
        + [{"$ref": f"#/definitions/{k}"} for k in IMPORTED.schema_executors.keys()],
        'definitions': definitions,
    }
