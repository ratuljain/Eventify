from lettuce import step, world


@step("I login with the following credentials:")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.payload = step.hashes[0]
