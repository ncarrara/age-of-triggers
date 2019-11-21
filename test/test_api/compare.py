import logging

logger = logging.getLogger(__name__)


def compare_scenario_files(copy, true, header=False):
    differences = []
    if header:
        true = true.variables_header
        copy = copy.variables_header
    else:
        true = true.variables
        copy = copy.variables

    keys_true = true.keys()
    keys_copy = copy.keys()

    for i, (key_true, key_copy) in enumerate(zip(keys_true, keys_copy)):
        true_value = true[key_true]
        copy_value = copy[key_copy]
        if true_value != copy_value:
            logger.debug(
                "Value are differents true[\"{}\"]={} != copy[\"{}\"]={}".format(key_true, true_value,
                                                                                 key_copy, copy_value))
            # exit(-1)
    # for offset, (key, value) in true.items():
    #     if continu == 0:
    #         try:
    #             key_copy, value_copy = copy[offset]
    #         except Exception:
    #             logging.error("Wrong offset for copy: {}".format(offset))
    #             continu = 50
    #         # exit(-1)
    #     if continu > 0:
    #         logger.debug("offset={} key={} value={}".format(offset, key, value))
    #         continu -= 1
    #         if continu == 0:
    #             exit(-1)
    #     else:
    #         if key != key_copy or value != value_copy:
    #             logger.debug("this offset doesn't match [{}], true[{}]={} and copy[{}]={}"
    #                          .format(offset, key, str(value)[:30], key_copy, str(value_copy)[:30]))
    #             differences.append(key)
    #         else:
    #             logger.debug("{} {} {} {}".format(key, value, key_copy, value_copy))
    return differences
