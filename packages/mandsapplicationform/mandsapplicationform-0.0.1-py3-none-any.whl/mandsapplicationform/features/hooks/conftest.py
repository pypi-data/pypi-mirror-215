from qashared.hooks import * 

def pytest_bdd_before_scenario(request, feature, scenario):
    set_test_context_before_scenario(request, feature, scenario)

def pytest_bdd_after_step(request, feature, scenario, step):
    screenshot_after_step(request, feature, scenario, step)

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    screenshot_after_step(request, feature, scenario, step, step_failed=True)