def set_test_context_before_scenario(request, feature, scenario):
    test_context = request.getfixturevalue('test_context')
    
    test_context.feature_name = feature.name.replace(' ', '_')
    test_context.scenario_name = scenario.name.replace(' ', '_')

def screenshot_after_step(request, feature, scenario, step, step_failed = False):
    feature_name = feature.name.replace(' ', '_')
    scenario_name = scenario.name.replace(' ', '_')
    step_name = step._name.replace(' ', '_')

    page = request.getfixturevalue('page')
    page.screenshot(path=f'./test_results/{feature_name}/{scenario_name}/screenshots/{"FAILED_" if step_failed else ""}{step_name}.png')