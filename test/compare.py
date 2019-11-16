import logging

logger = logging.getLogger(__name__)


def compare_scenario_files(scn_to_check, true_scn):
    differences = []
    for key, value in true_scn.variables.items():
        if value != scn_to_check.variables[key]:
            logger.debug("this key doesn't match [{}], <{}> should be <{}>"
                         .format(key, str(scn_to_check.variables[key])[:30], str(value)[:30]))
            differences.append(key)
    return differences
