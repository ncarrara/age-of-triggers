import logging

logger = logging.getLogger(__name__)


def compare_scenario_files(scn_to_check, true_scn, header=False):
    differences = []
    if header:
        true = true_scn.variables_header
        copy = scn_to_check.variables_header
    else:
        true = true_scn.variables
        copy = scn_to_check.variables
    for offset, (key, value) in true.items():
        key_copy, value_copy = copy[offset]
        if key != key_copy:
            logger.debug("this offset doesn't match [{}], true[{}]={} and copy[{}]={}"
                         .format(offset, key, str(value)[:30], key_copy, str(value_copy)[:30]))
            differences.append(key)
    return differences
