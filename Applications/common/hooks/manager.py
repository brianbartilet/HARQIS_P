from Core.utilities.custom_logger import custom_logger
import sys, os

log = custom_logger(logger_name="Hooks Manager")


class HooksManager(object):
    hooks = []


def before_all(context):
    _execute_hooks(before_all.__name__, HooksManager.hooks, [context])


def before_feature(context, feature):
    _execute_hooks(before_feature.__name__, HooksManager.hooks, [context, feature])


def before_scenario(context, scenario):
    _execute_hooks(before_scenario.__name__, HooksManager.hooks, [context, scenario])


def before_step(context, step):
    _execute_hooks(before_step.__name__, HooksManager.hooks, [context, step])


def after_all(context):
    _execute_hooks(after_all.__name__, HooksManager.hooks, [context])


def after_feature(context, feature):
    _execute_hooks(after_feature.__name__, HooksManager.hooks, [context, feature])


def after_scenario(context, scenario):
    _execute_hooks(after_scenario.__name__, HooksManager.hooks, [context, scenario])


def after_step(context, step):
    _execute_hooks(after_step.__name__, HooksManager.hooks, [context, step])


def _execute_hooks(method_name, hooks_sequence, context_arg_list):

    for hook in hooks_sequence:
        try:
            obj = hook()
            getattr(obj, method_name)(*context_arg_list)

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_hook_target = exc_tb.tb_next
            file = os.path.split(error_hook_target.tb_frame.f_code.co_filename)[1]
            line = error_hook_target.tb_lineno
            msg = str(exc_obj)

            log.warning("HOOKS EXCEPTION: " + file + "  line: " + str(line) + "  message: " + msg + "\n")
